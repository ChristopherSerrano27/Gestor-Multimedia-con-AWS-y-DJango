# Generated by Django 5.1.1 on 2024-09-28 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_media", "0010_alter_archivo_archivo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="archivo",
            name="archivo",
            field=models.FileField(upload_to=""),
        ),
    ]
