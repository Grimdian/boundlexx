# Generated by Django 3.1.2 on 2020-11-03 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boundless', '0045_beacon_beaconplotcolumn_beaconscan'),
    ]

    operations = [
        migrations.AddField(
            model_name='beaconscan',
            name='html_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='beaconscan',
            name='text_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
