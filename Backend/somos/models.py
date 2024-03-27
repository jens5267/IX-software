from django.db import models
from datetime import datetime, timedelta

class Simulation(models.Model):
    start_date = models.DateTimeField()
    time_passed = models.FloatField(default=0)

    def tick(self):
        self.time_passed += 0.25

    def simulate(self, end_date):
        if end_date >= self.start_date:
            time_difference = (datetime(end_date) - datetime(self.start_date)).total_seconds()/(4*60)
        
        for quarter in time_difference:
            self.tick()



class Port(models.Model):
    name = models.CharField(max_length = 100)

class WindTurbine(models.Model):
    name = models.CharField(max_length=100)

class WindFarm(models.Model):
    turbine = models.ForeignKey(WindTurbine, on_delete=models.CASCADE)

class SparePart(models.Model):
    name = models.CharField(max_length=140)

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    spare_parts = models.ManyToManyField(SparePart, through='WarehouseSparePart')

class WarehouseSparePart(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

class Vessel(models.Model):
    name = models.CharField(max_length=100)
    spare_parts = models.ManyToManyField(SparePart, through='VesselSparePart')

class VesselSparePart(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def prepare_for_repair(self, vessel, spare_part, quantity):
        # Remove spare parts from warehouse and associate them with the vessel
        warehouse_spare_part = WarehouseSparePart.objects.filter(warehouse__spare_parts=spare_part).first()
        if warehouse_spare_part:
            if warehouse_spare_part.quantity >= quantity:
                warehouse_spare_part.quantity -= quantity
                warehouse_spare_part.save()
                vessel_spare_part, created = VesselSparePart.objects.get_or_create(vessel=vessel, spare_part=spare_part)
                vessel_spare_part.quantity += quantity
                vessel_spare_part.save()
                return True
        return False    