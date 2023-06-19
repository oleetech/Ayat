from django.db import models

# Create your models here.
class BillOfMaterials(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    bomtype = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)

class ChildComponent(models.Model):
    bill_of_materials = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE, related_name='child_components')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    uom = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)


class Production(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name

class ProductionComponent(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='production_components')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    uom = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name

