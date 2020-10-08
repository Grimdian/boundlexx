from rest_framework import serializers

from boundlexx.boundless.models import (
    LocalizedName,
    LocalizedString,
    LocalizedStringText,
)


class NullSerializer(serializers.Serializer):
    def create(self, validated_data):
        return

    def update(self, instance, validated_data):
        return


class AzureImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None

        try:
            url = value.url
        except AttributeError:
            return None

        return url


class LangFilterListSerializer(
    serializers.ListSerializer
):  # pylint: disable=abstract-method
    def to_representation(self, data):
        data = super().to_representation(data)
        lang = self.context["request"].query_params.get("lang", "all")

        if lang == "all":
            return data
        if lang == "none":
            return []

        new_data = []
        for item in data:
            if item["lang"] == lang:
                new_data.append(item)
        data = new_data

        return data


class LocalizedStringTextSerializer(serializers.ModelSerializer):
    plain_text = serializers.CharField()

    class Meta:
        model = LocalizedStringText
        list_serializer_class = LangFilterListSerializer
        fields = ["lang", "text", "plain_text"]


class LocalizedStringSerializer(serializers.ModelSerializer):
    strings = LocalizedStringTextSerializer(many=True)

    class Meta:
        model = LocalizedString
        list_serializer_class = LangFilterListSerializer
        fields = ["string_id", "strings"]


class LocalizedNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalizedName
        list_serializer_class = LangFilterListSerializer
        fields = ["lang", "name"]