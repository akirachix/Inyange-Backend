# Generated by Django 5.1.1 on 2024-09-20 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_payment_checkout_request_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
    ]
