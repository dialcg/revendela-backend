# Generated by Django 5.0.4 on 2025-02-25 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0008_alter_ticket_last_status_change"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="last_status_change",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Último cambio de estado"
            ),
        ),
    ]
