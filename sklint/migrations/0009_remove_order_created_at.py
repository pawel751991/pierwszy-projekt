# Generated by Django 3.2.4 on 2021-07-02 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sklint', '0008_remove_order_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='created_at',
        ),
    ]
