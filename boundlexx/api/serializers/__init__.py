from rest_framework import serializers

from boundlexx.api.serializers.base import NullSerializer, SimpleWorldSerializer
from boundlexx.api.serializers.game import (
    ColorSerializer,
    EmojiSerializer,
    GameFileSerializer,
    ItemResourceCountSerializer,
    ItemResourceCountTimeSeriesSerializer,
    ItemSerializer,
    SimpleGameFileSerializer,
    SimpleItemRequestBasketPriceSerializer,
    SimpleItemShopPriceSerializer,
    SimpleItemShopStandPriceSerializer,
    SimpleWorldRequestBasketPriceSerializer,
    SimpleWorldShopPriceSerializer,
    SimpleWorldShopStandPriceSerializer,
    SkillGroupSerializer,
    SkillSerializer,
    SubtitleSerializer,
)
from boundlexx.api.serializers.world import (
    BlockColorSerializer,
    ItemColorSerializer,
    ItemResourceCountTimeSeriesTBSerializer,
    LeaderboardSerializer,
    ResourcesSerializer,
    WorldBlockColorSerializer,
    WorldBlockColorsViewSerializer,
    WorldColorSerializer,
    WorldDistanceSerializer,
    WorldPollExtraSerializer,
    WorldPollLeaderboardSerializer,
    WorldPollResourcesSerializer,
    WorldPollSerializer,
    WorldPollTBSerializer,
    WorldSerializer,
)

__all__ = [
    "BlockColorSerializer",
    "ColorSerializer",
    "EmojiSerializer",
    "ForumFormatSerialzier",
    "GameFileSerializer",
    "ItemColorSerializer",
    "ItemResourceCountSerializer",
    "ItemResourceCountTimeSeriesSerializer",
    "ItemResourceCountTimeSeriesTBSerializer",
    "ItemSerializer",
    "LeaderboardSerializer",
    "ResourcesSerializer",
    "SimpleGameFileSerializer",
    "SimpleItemRequestBasketPriceSerializer",
    "SimpleItemShopPriceSerializer",
    "SimpleItemShopStandPriceSerializer",
    "SimpleWorldRequestBasketPriceSerializer",
    "SimpleWorldSerializer",
    "SimpleWorldShopPriceSerializer",
    "SimpleWorldShopStandPriceSerializer",
    "SkillGroupSerializer",
    "SkillSerializer",
    "SubtitleSerializer",
    "WorldBlockColorSerializer",
    "WorldBlockColorsViewSerializer",
    "WorldColorSerializer",
    "WorldDistanceSerializer",
    "WorldPollExtraSerializer",
    "WorldPollLeaderboardSerializer",
    "WorldPollResourcesSerializer",
    "WorldPollSerializer",
    "WorldPollTBSerializer",
    "WorldSerializer",
]


class ForumFormatSerialzier(NullSerializer):
    title = serializers.CharField(read_only=True)
    body = serializers.CharField(read_only=True)