# Generated by Django 3.0.5 on 2020-04-13 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("django_celery_results", "0007_remove_taskresult_hidden"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskOutput",
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
                ("output", models.TextField(verbose_name="Task Output")),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_celery_results.TaskResult",
                    ),
                ),
            ],
        ),
    ]
