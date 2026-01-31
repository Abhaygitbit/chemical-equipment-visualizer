from django.db import models
from django.utils import timezone

class Dataset(models.Model):
    """Stores information about uploaded CSV files"""
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(default=timezone.now)
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    type_distribution = models.JSONField(default=dict)
    file_path = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.filename} - {self.upload_date}"

class Equipment(models.Model):
    """Stores individual equipment data"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return f"{self.name} ({self.equipment_type})"