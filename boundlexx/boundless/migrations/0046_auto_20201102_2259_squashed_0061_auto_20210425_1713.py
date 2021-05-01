# Generated by Django 3.2 on 2021-05-01 15:37

from django.db import migrations, models
import django.db.models.deletion
import storages.backends.azure_storage


class Migration(migrations.Migration):
    dependencies = [
        ("boundless", "0045_beacon_beaconplotcolumn_beaconscan"),
    ]

    operations = [
        migrations.AddField(
            model_name="beaconscan",
            name="text_name",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="beaconscan",
            name="html_name",
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.RemoveField(
            model_name="emoji",
            name="is_boundless_only",
        ),
        migrations.AddField(
            model_name="emoji",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("SMILEY", "Smiley & Emotion"),
                    ("PEOPLE", "People & Body"),
                    ("COMPONENT", "Component"),
                    ("ANIMAL", "Animals & Nature"),
                    ("FOOD", "Food & Drink"),
                    ("TRAVEL", "Travel & Places"),
                    ("ACTIVITIES", "Activities"),
                    ("OBJECTS", "Objects"),
                    ("SYMBOLS", "Symbols"),
                    ("FLAGS", "Flags"),
                    ("BOUNDLESS", "Boundless"),
                    ("UNCATEGORIZED", "Uncategorized"),
                ],
                db_index=True,
                max_length=16,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="itemrequestbasketprice",
            name="guild_tag",
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name="itemshopstandprice",
            name="guild_tag",
            field=models.CharField(max_length=16),
        ),
        migrations.AlterModelOptions(
            name="world",
            options={
                "ordering": ["id"],
                "permissions": [("can_view_private", "Can view private worlds?")],
            },
        ),
        migrations.AddField(
            model_name="item",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=storages.backends.azure_storage.AzureStorage(
                    azure_container="local-items"
                ),
                upload_to="",
            ),
        ),
        migrations.AddField(
            model_name="emoji",
            name="image_small",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=storages.backends.azure_storage.AzureStorage(
                    azure_container="local-emoji"
                ),
                upload_to="",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="image_small",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=storages.backends.azure_storage.AzureStorage(
                    azure_container="local-items"
                ),
                upload_to="",
            ),
        ),
        migrations.CreateModel(
            name="ItemColorVariant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        storage=storages.backends.azure_storage.AzureStorage(
                            azure_container="local-items"
                        ),
                        upload_to="",
                    ),
                ),
                (
                    "color",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="boundless.color",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="boundless.item"
                    ),
                ),
                (
                    "image_small",
                    models.ImageField(
                        blank=True,
                        null=True,
                        storage=storages.backends.azure_storage.AzureStorage(
                            azure_container="local-items"
                        ),
                        upload_to="",
                    ),
                ),
            ],
            options={
                "unique_together": {("item", "color")},
            },
        ),
        migrations.AddField(
            model_name="world",
            name="image_small",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=storages.backends.azure_storage.AzureStorage(
                    azure_container="local-worlds"
                ),
                upload_to="",
            ),
        ),
        migrations.CreateModel(
            name="ItemMetalVariant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        storage=storages.backends.azure_storage.AzureStorage(
                            azure_container="local-items"
                        ),
                        upload_to="",
                    ),
                ),
                (
                    "image_small",
                    models.ImageField(
                        blank=True,
                        null=True,
                        storage=storages.backends.azure_storage.AzureStorage(
                            azure_container="local-items"
                        ),
                        upload_to="",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="boundless.item"
                    ),
                ),
                (
                    "metal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="boundless.metal",
                    ),
                ),
            ],
            options={
                "unique_together": {("item", "metal")},
            },
        ),
        migrations.AddField(
            model_name="item",
            name="default_color",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="boundless.color",
            ),
        ),
        migrations.AddField(
            model_name="world",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name="Settlement",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location_x", models.IntegerField()),
                ("location_z", models.IntegerField()),
                ("prestige", models.PositiveIntegerField(db_index=True, default=None)),
                ("name", models.CharField(default=None, max_length=64)),
                ("text_name", models.CharField(blank=True, max_length=64, null=True)),
                ("html_name", models.CharField(blank=True, max_length=1024, null=True)),
                (
                    "world",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="boundless.world",
                    ),
                ),
            ],
            options={
                "unique_together": set(),
            },
        ),
    ]