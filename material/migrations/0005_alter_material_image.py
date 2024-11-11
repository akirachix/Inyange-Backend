# Generated by Django 5.1.1 on 2024-11-08 14:11

import material.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("material", "0004_alter_material_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="material",
            name="image",
            field=models.ImageField(
                default=1,
                upload_to="materials_images/",
                validators=[material.models.validate_image_format],
            ),
            preserve_default=False,
        ),
    ]