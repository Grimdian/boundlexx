# Generated by Django 3.1.3 on 2020-11-02 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boundless', '0044_item_is_block'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beacon',
            fields=[
                ('time', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('is_campfire', models.BooleanField()),
                ('location_x', models.IntegerField()),
                ('location_y', models.IntegerField()),
                ('location_z', models.IntegerField()),
                ('world', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boundless.world')),
            ],
            options={
                'unique_together': {('time', 'world', 'location_x', 'location_y', 'location_z')},
            },
        ),
        migrations.CreateModel(
            name='BeaconScan',
            fields=[
                ('time', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False)),
                ('mayor_name', models.CharField(max_length=64)),
                ('prestige', models.PositiveIntegerField(blank=True, null=True)),
                ('compactness', models.SmallIntegerField(blank=True, null=True)),
                ('num_plots', models.PositiveIntegerField(blank=True, null=True)),
                ('num_columns', models.PositiveIntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('beacon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boundless.beacon')),
            ],
            options={
                'unique_together': {('time', 'beacon')},
            },
        ),
        migrations.CreateModel(
            name='BeaconPlotColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot_x', models.IntegerField()),
                ('plot_z', models.IntegerField()),
                ('count', models.PositiveSmallIntegerField()),
                ('beacon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boundless.beacon')),
            ],
            options={
                'unique_together': {('beacon', 'plot_x', 'plot_z')},
            },
        ),

        migrations.RunSQL(
            'ALTER TABLE "boundless_beaconscan" DROP CONSTRAINT "boundless_beaconscan_pkey"', reverse_sql=migrations.RunSQL.noop
        ),
        migrations.RunSQL(
            "SELECT create_hypertable('boundless_beaconscan', 'time', chunk_time_interval => 86400000000, migrate_data => true, create_default_indexes => false)", reverse_sql=migrations.RunSQL.noop
        ),
    ]
