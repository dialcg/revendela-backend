# Generated by Django 5.0.4 on 2025-02-25 23:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0009_alter_ticket_last_status_change"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="created_time",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Tiempo de creación",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="ticket",
            name="last_status_change",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Último cambio de estado"
            ),
        ),
    ]
