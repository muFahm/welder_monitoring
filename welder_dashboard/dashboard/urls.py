# dashboard/urls.py
from django.urls import path
from .views import dashboard_view, SensorRecordAPIView, ActivityPredictionAPIView, StartSessionAPIView, StopSessionAPIView, ActivityStatsAPIView

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('api/sensor-data/', SensorRecordAPIView.as_view(), name='sensor-data-api'),
    path('api/predict-activity/', ActivityPredictionAPIView.as_view(), name='predict-activity-api'),
    path('api/start-session/', StartSessionAPIView.as_view(), name='start-session'),
    path('api/stop-session/', StopSessionAPIView.as_view(), name='stop-session'),
    path('api/activity-stats/', ActivityStatsAPIView.as_view(), name='activity-stats'),

]
