# Generated by Django 4.2.2 on 2023-06-20 17:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartners', '0001_initial'),
        ('Sales', '0003_alter_salesorderinfo_totalamount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryInfo',
            fields=[
                ('SalesOrder', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Sales.salesorderinfo')),
                ('Address', models.CharField(max_length=50)),
                ('Created', models.DateTimeField(default=django.utils.timezone.now)),
                ('DocNo', models.PositiveIntegerField(default=1, unique=True)),
                ('TotalAmount', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True)),
                ('CustomerName', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BusinessPartners.businesspartner')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SalesOrder', models.PositiveIntegerField(default=1)),
                ('ItemCode', models.CharField(max_length=20)),
                ('ItemName', models.CharField(max_length=50)),
                ('Quantity', models.PositiveIntegerField(default=0)),
                ('Price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('PriceTotal', models.DecimalField(decimal_places=4, max_digits=10)),
                ('Delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sales.deliveryinfo')),
            ],
        ),
    ]
