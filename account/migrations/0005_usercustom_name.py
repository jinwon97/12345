# Generated by Django 4.2 on 2024-01-06 07:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0004_loginfo_isadmin"),
    ]

    operations = [
        migrations.AddField(
            model_name="usercustom",
            name="name",
            field=models.CharField(default="dave the QA tester", max_length=25),
        ),
    ]
