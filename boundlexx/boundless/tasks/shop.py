import hashlib
from collections import namedtuple
from typing import Dict, List

from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone

from boundlexx.boundless.client import HTTP_ERRORS, BoundlessClient
from boundlexx.boundless.client import World as SimpleWorld
from boundlexx.boundless.models import (
    Color,
    Item,
    ItemBuyRank,
    ItemRank,
    ItemRequestBasketPrice,
    ItemSellRank,
    ItemShopStandPrice,
    World,
)
from config.celery_app import app

logger = get_task_logger(__name__)


UpdateOption = namedtuple(
    "UpdateOption", ("rank_klass", "client_method", "price_klass")
)


UPDATE_PRICES_LOCK = "boundless:update_prices"
WORLDS_QUEUED_LOCK = "boundless:prices:update_worlds"
WORLDS_QUEUED_CACHE = "boundless:prices:worlds"


def _get_queued_worlds():
    with cache.lock(WORLDS_QUEUED_LOCK, expire=10, auto_renewal=False):
        return list(cache.get(WORLDS_QUEUED_CACHE, set()))


def _update_queued_worlds(worlds):
    actual_worlds = []
    with cache.lock(WORLDS_QUEUED_LOCK, expire=10, auto_renewal=False):
        in_progress_ids = cache.get(WORLDS_QUEUED_CACHE, set())

        for world in worlds:
            if world.id not in in_progress_ids:
                in_progress_ids.add(world.id)
                actual_worlds.append(world)

        cache.set(WORLDS_QUEUED_CACHE, in_progress_ids, timeout=21600)

    return actual_worlds


def _remove_queued_worlds(worlds):
    with cache.lock(WORLDS_QUEUED_LOCK, expire=10, auto_renewal=False):
        in_progress_ids = cache.get(WORLDS_QUEUED_CACHE, set())

        for world in worlds:
            in_progress_ids.discard(world.id)

        cache.set(WORLDS_QUEUED_CACHE, in_progress_ids, timeout=21600)


@app.task
def update_prices(world_ids=None):
    queued_ids = _get_queued_worlds()

    if world_ids is None:
        worlds = (
            World.objects.filter(active=True, is_creative=False, api_url__isnull=False)
            .filter(
                Q(end__isnull=True)
                | Q(
                    is_locked=False,
                    end__isnull=False,
                    end__gt=timezone.now(),
                    owner__isnull=False,
                    is_public=True,
                )
            )
            .exclude(api_url="")
            .exclude(id__in=queued_ids)
        )
    else:
        worlds = World.objects.filter(id__in=world_ids).order_by("id")

    _update_prices_multi(worlds)


@app.task
def update_prices_split(world_ids):
    worlds = World.objects.filter(id__in=world_ids).order_by("id")

    first = worlds.first()

    if first is None:
        return

    count = worlds.count()

    _update_prices_multi(worlds, f"{first.id}:{count}")


def _update_prices_multi(worlds, name=None):
    lock_name = UPDATE_PRICES_LOCK

    if name is not None:
        lock_name = f"{lock_name}:{name}"

    lock = cache.lock(lock_name, expire=120, auto_renewal=False)

    acquired = lock.acquire(blocking=True, timeout=1)

    if not acquired:
        return

    try:
        _update_prices(worlds)
    finally:
        try:
            lock.release()
        except Exception as ex:  # pylint: disable=broad-except
            logger.warning("Could not release lock: %s", ex)


def _get_ranks(item, rank_klass, all_worlds):
    ranks: Dict[str, ItemRank] = {}
    worlds: List[SimpleWorld] = []

    now = timezone.now()

    for world in all_worlds:
        rank, _ = rank_klass.objects.get_or_create(item=item, world=world)
        if rank.next_update < now:
            ranks[world.name] = rank
            worlds.append(SimpleWorld(world.name, world.api_url))

    return ranks, worlds


def _create_item_prices(shops, price_klass, world_name, item):
    shops = sorted(
        shops,
        key=lambda s: f"{s.location.x},{s.location.y},{s.location.z}",
    )

    colors = Color.objects.all()

    total = 0
    state_hash = hashlib.sha512()
    for shop in shops:
        item_price = price_klass.objects.create_from_shop_item(
            world_name, item, shop, colors=colors
        )

        state_hash.update(item_price.state_hash)
        total += 1

    return total, state_hash


def _update_item_prices(item, rank_klass, client_method, price_klass, all_worlds):

    client = BoundlessClient()
    ranks, worlds = _get_ranks(item, rank_klass, all_worlds)

    if len(ranks) == 0:
        return -1

    total = 0
    shops = getattr(client, client_method)(item.game_id, worlds=worlds)

    # set all existing price records to inactive
    price_klass.objects.filter(
        item=item, active=True, world__name__in=list(ranks.keys())
    ).update(active=False)

    for world_name, shops in shops.items():
        item_total, state_hash = _create_item_prices(
            shops, price_klass, world_name, item
        )
        total += item_total

        digest = str(state_hash.hexdigest())
        rank = ranks[world_name]
        if rank.state_hash != "":
            if rank.state_hash == digest:
                rank.decrease_rank()
            else:
                rank.increase_rank()

        rank.state_hash = digest
        rank.last_update = timezone.now()
        rank.save()

    return total


def _log_worlds(all_worlds):
    worlds = []
    for world in all_worlds:
        worlds.append((world.name, world.api_url))

    logger.info("All worlds: %s", worlds)


def _split_update_prices(worlds):
    max_sov_worlds = settings.BOUNDLESS_MAX_SOV_WORLDS_PER_PRICE_POLL
    max_perm_worlds = settings.BOUNDLESS_MAX_PERM_WORLDS_PER_PRICE_POLL

    worlds = list(worlds)
    run = 1
    while len(worlds) > max_sov_worlds or (
        len(worlds) > 1 and worlds[0].is_perm and len(worlds) > max_perm_worlds
    ):
        max_worlds = max_sov_worlds
        if worlds[0].is_perm:
            max_worlds = max_perm_worlds

        worlds_ids = [w.id for w in worlds[:max_worlds]]
        logger.info("Run %s: %s", run, worlds_ids)
        update_prices_split.delay(worlds_ids)
        worlds = worlds[max_worlds:]
        run += 1

    if len(worlds) > 0:
        worlds_ids = [w.id for w in worlds]
        logger.info("Run %s: %s", run, worlds_ids)
        update_prices_split.delay(worlds_ids)


def _update_prices(worlds):
    total = len(worlds)
    if total > settings.BOUNDLESS_MAX_SOV_WORLDS_PER_PRICE_POLL:
        _split_update_prices(worlds)
        return

    worlds = _update_queued_worlds(worlds)
    items = Item.objects.filter(active=True, can_be_sold=True)
    logger.info("Updating the prices for %s items", len(items))

    _log_worlds(worlds)

    errors_total = 0

    try:
        for item in items:
            try:
                buy_updated = _update_item_prices(
                    item,
                    ItemBuyRank,
                    "shop_buy",
                    ItemRequestBasketPrice,
                    worlds,
                )
            except HTTP_ERRORS as ex:
                errors_total += 1
                buy_updated = -2
                logger.error("%s while updating buy prices of %s", ex, item)

            try:
                sell_updated = _update_item_prices(
                    item, ItemSellRank, "shop_sell", ItemShopStandPrice, worlds
                )
            except HTTP_ERRORS as ex:
                errors_total += 1
                sell_updated = -2
                logger.error("%s while updating sell prices of %s", ex, item)

            if buy_updated >= -1 or sell_updated >= -1:
                if buy_updated == -1 and sell_updated == -1:
                    logger.info("Skipped %s", item)
                else:

                    def status(v):
                        return v if v >= 0 else "skipped" if v == -1 else "error"

                    logger.info(
                        "Updated %s (Baskets: %s, Stands: %s)",
                        item,
                        status(buy_updated),
                        status(sell_updated),
                    )

            if errors_total > 10:
                raise Exception("Aborting due to large number of HTTP errors")
    finally:
        _remove_queued_worlds(worlds)
