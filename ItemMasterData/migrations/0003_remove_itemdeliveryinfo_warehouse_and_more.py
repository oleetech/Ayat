# Generated by Django 4.2.2 on 2023-06-23 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ItemMasterData', '0002_remove_item_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemdeliveryinfo',
            name='warehouse',
        ),
        migrations.RemoveField(
            model_name='itemreceiptinfo',
            name='warehouse',
        ),
    ]
