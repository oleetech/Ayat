# Generated by Django 4.2.1 on 2023-06-24 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ItemMasterData', '0003_remove_itemdeliveryinfo_warehouse_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='code',
            field=models.CharField(default='', max_length=25, unique=True),
        ),
    ]
