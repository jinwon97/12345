# Generated by Django 4.2 on 2024-01-05 12:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("faq", "0002_user"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Admin",
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
