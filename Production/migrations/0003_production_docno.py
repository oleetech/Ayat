# Generated by Django 4.2.1 on 2023-06-19 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0002_production_created_date_production_due_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='production',
            name='docno',
            field=models.PositiveIntegerField(default=1, unique=True),
        ),
    ]
