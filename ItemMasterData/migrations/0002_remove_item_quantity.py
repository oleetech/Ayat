# Generated by Django 4.2.2 on 2023-06-23 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ItemMasterData', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
    ]