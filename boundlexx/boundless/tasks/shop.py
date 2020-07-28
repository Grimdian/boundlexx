import hashlib
from collections import namedtuple
from typing import Dict

from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone

from boundlexx.boundless.client import BoundlessClient
from boundlexx.boundless.models import (
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


@app.task
def try_update_prices():
    lock = cache.lock(UPDATE_PRICES_LOCK)

    acquired = lock.acquire(blocking=True, timeout=1)

    if acquired:
        try:
            _update_prices()
        finally:
            lock.release()
    else:
        logger.warning("Could not update prices, task already running")


def _get_ranks(item, rank_klass, all_worlds):
    ranks: Dict[str, ItemRank] = {}

    now = timezone.now()

    for world in all_worlds:
        rank, _ = rank_klass.objects.get_or_create(item=item, world=world)
        if rank.next_update < now:
            ranks[world.name] = rank

    return ranks


def _update_item_prices(
    item, rank_klass, client_method, price_klass, all_worlds
):

    client = BoundlessClient()
    ranks = _get_ranks(item, rank_klass, all_worlds)

    if len(ranks) == 0:
        return -1

    total = 0
    shops = getattr(client, client_method)(
        item.game_id, worlds=list(ranks.keys())
    )

    # set all existing price records to inactive
    price_klass.objects.filter(
        item=item, active=True, world__name__in=list(ranks.keys())
    ).update(active=False)

    for world_name, shops in shops.items():
        state_hash = hashlib.sha512()

        shops = sorted(shops, key=lambda s: s.location)
        for shop in shops:
            item_price = price_klass.from_shop_item(world_name, item, shop)

            state_hash.update(item_price.state_hash)
            total += 1

        digest = str(state_hash.hexdigest())
        rank = ranks[world_name]
        if rank.state_hash == digest:
            rank.decrease_rank()
        else:
            rank.increase_rank()

        rank.state_hash = digest
        rank.last_update = timezone.now()
        rank.save()

    return total


def _update_prices():
    items = Item.objects.filter(active=True)
    logger.info("Updating the prices for %s items", len(items))

    all_worlds = list(
        World.objects.filter(active=True, is_creative=False).filter(
            Q(owner__isnull=False) | Q(end__isnull=True)
        )
    )
    for item in items:
        buy_updated = _update_item_prices(
            item, ItemBuyRank, "shop_buy", ItemRequestBasketPrice, all_worlds
        )
        sell_updated = _update_item_prices(
            item, ItemSellRank, "shop_sell", ItemShopStandPrice, all_worlds
        )

        if buy_updated >= 0 or sell_updated >= 0:
            logger.info(
                "Updated %s (Baskets: %s, Stands: %s)",
                item,
                buy_updated,
                sell_updated,
            )
        else:
            logger.info("Skipped %s", item)
