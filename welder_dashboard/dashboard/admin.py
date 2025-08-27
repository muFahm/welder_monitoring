from django.contrib import admin
from dashboard.models import PredictionResult, SensorRecord
# Register your models here.
admin.site.register(PredictionResult)
admin.site.register(SensorRecord)