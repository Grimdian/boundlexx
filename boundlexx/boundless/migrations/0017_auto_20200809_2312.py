# Generated by Django 3.0.9 on 2020-08-10 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boundless', '0016_resourcecount_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='world',
            name='world_type',
            field=models.CharField(choices=[('LUSH', 'Lush'), ('METAL', 'Metal'), ('COAL', 'Coal'), ('CORROSIVE', 'Corrosive'), ('SHOCK', 'Shock'), ('BLAST', 'Blast'), ('TOXIC', 'Toxic'), ('CHILL', 'Chill'), ('BURN', 'Burn'), ('UMBRIS', 'Umbris'), ('RIFT', 'Rift'), ('BLINK', 'Blink')], db_index=True, max_length=10, null=True, verbose_name='World Type'),
        ),
    ]
