# Generated by Django 5.1.1 on 2024-09-23 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='material_name',
            field=models.CharField(max_length=255),
        ),
    ]
