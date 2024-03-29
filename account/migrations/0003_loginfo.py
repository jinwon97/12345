# Generated by Django 4.2 on 2024-01-04 22:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_alter_usercustom_password"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogInfo",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("isLogedIn", models.BooleanField(default=False)),
                ("logtime", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
