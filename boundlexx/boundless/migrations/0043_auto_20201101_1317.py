# Generated by Django 3.1.2 on 2020-11-01 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boundless', '0042_remove_resourcecount_fixed_average'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcedatabestworld',
            name='data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='best_worlds', to='boundless.resourcedata'),
        ),
    ]
