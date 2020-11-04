# Generated by Django 3.1.2 on 2020-11-04 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boundless', '0048_auto_20201104_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emoji',
            name='category',
            field=models.CharField(blank=True, choices=[('SMILEY', 'Smiley & Emotion'), ('PEOPLE', 'People & Body'), ('COMPONENT', 'Component'), ('ANIMAL', 'Animals & Nature'), ('FOOD', 'Food & Drink'), ('TRAVEL', 'Travel & Places'), ('ACTIVITES', 'Activies'), ('OBJECTS', 'Objects'), ('SYMBOLS', 'Symbols'), ('FLAGS', 'Flags'), ('BOUNDLESS', 'Boundless'), ('UNCATEGORIZED', 'Uncategorized')], db_index=True, max_length=16, null=True),
        ),
    ]