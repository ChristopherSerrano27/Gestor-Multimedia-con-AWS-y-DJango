# Generated by Django 5.1.1 on 2024-09-28 19:49

import app_media.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_media", "0011_alter_archivo_archivo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="archivo",
            name="archivo",
            field=models.FileField(upload_to=app_media.models.user_directory_path),
        ),
    ]
