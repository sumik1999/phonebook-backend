# Generated by Django 3.2.12 on 2022-02-10 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_globalcontact"),
    ]

    operations = [
        migrations.AlterField(
            model_name="globalcontact",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="owner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
