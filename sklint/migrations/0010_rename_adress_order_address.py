# Generated by Django 3.2.4 on 2021-07-02 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sklint', '0009_remove_order_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='adress',
            new_name='address',
        ),
    ]
