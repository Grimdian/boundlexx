# Generated by Django 3.1.2 on 2020-10-29 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boundless', '0035_world_map_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='world',
            old_name='map_image',
            new_name='atlas_image',
        ),
    ]
