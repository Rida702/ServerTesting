# Generated by Django 4.2 on 2023-12-31 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imageApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="imagemodel",
            name="grayscale_image",
            field=models.ImageField(blank=True, upload_to="grayscaled/"),
        ),
    ]
