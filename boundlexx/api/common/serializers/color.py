from rest_framework import serializers

from boundlexx.api.common.serializers.base import LocalizedNameSerializer
from boundlexx.boundless.models import Color


class IDColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = [
            "game_id",
        ]


class ColorSerializer(serializers.ModelSerializer):
    localization = LocalizedNameSerializer(
        source="localizedname_set",
        many=True,
    )
    base_color = serializers.CharField()
    gleam_color = serializers.CharField()

    class Meta:
        model = Color
        fields = [
            "game_id",
            "base_color",
            "gleam_color",
            "localization",
        ]
