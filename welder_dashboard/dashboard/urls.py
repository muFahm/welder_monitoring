# dashboard/urls.py
from django.urls import path
from .views import (
    dashboard_view, 
    SensorRecordAPIView,
    LatestSensorAPIView,
    ActivityPredictionAPIView,
    ActivityStatsAPIView,
    WelderProfileAPIView
)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    
    # sensor
    path('api/sensor-data/', SensorRecordAPIView.as_view(), name='sensor-data-api'),
    path('api/sensor/latest/', LatestSensorAPIView.as_view(), name='sensor-latest-api'),
    
    # prediksi & statistik
    path('api/predict-activity/', ActivityPredictionAPIView.as_view(), name='predict-activity-api'),
    path('api/activity-stats/', ActivityStatsAPIView.as_view(), name='activity-stats'),
    
    # welder profile
    path('api/welder/', WelderProfileAPIView.as_view(), name='welder-list-api'),
    path('api/welder/<int:welder_id>/', WelderProfileAPIView.as_view(), name='welder-detail-api'),]
