from django.contrib import admin
from dashboard.models import WeldingSession, PredictionResult, SensorRecord
# Register your models here.
admin.site.register(WeldingSession)
admin.site.register(PredictionResult)
admin.site.register(SensorRecord)