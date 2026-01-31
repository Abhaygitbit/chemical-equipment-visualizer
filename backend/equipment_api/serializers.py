from rest_framework import serializers
from .models import Dataset, Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='equipment_type')
    
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'type', 'flowrate', 'pressure', 'temperature']

class DatasetSerializer(serializers.ModelSerializer):
    equipment_list = EquipmentSerializer(source='equipment', many=True, read_only=True)
    averages = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'upload_date', 'total_count', 'averages', 
                  'type_distribution', 'equipment_list']
    
    def get_averages(self, obj):
        return {
            'flowrate': round(obj.avg_flowrate, 2),
            'pressure': round(obj.avg_pressure, 2),
            'temperature': round(obj.avg_temperature, 2)
        }