# Generated by Django 5.0.4 on 2025-02-14 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authy", "0006_wallet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="balance",
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
        ),
    ]
