# welder_dashboard/dashboard/serializers.py
from rest_framework import serializers
from .models import SensorRecord

class SensorRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorRecord
        fields = '__all__'
