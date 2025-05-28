# dashboard/urls.py
from django.urls import path
from .views import dashboard_view, SensorRecordAPIView

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('api/sensor-data/', SensorRecordAPIView.as_view(), name='sensor-data-api'),
]
