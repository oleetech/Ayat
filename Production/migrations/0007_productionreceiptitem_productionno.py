# Generated by Django 4.2.2 on 2023-06-19 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0006_productionreceipt_alter_production_docno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionreceiptitem',
            name='ProductionNo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='production_receipt_components', to='Production.production'),
        ),
    ]
