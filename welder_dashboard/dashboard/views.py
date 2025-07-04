from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SensorRecord
from .serializers import SensorRecordSerializer
from .prediction_pipeline.predict import predict_latest_activity

# Tambahan untuk prediksi
from django.http import JsonResponse


def dashboard_view(request):
    return render(request, 'dashboard/index.html')

class SensorRecordAPIView(APIView):
    def get(self, request, format=None):
        data = SensorRecord.objects.order_by('-timestamp')[:250]  # Ambil 250 data terakhir
        serializer = SensorRecordSerializer(data, many=True)
        return Response(serializer.data)
    
class ActivityPredictionAPIView(APIView):
    def get(self, request, format=None):
        try:
            predicted_label = predict_latest_activity()  # Fungsi ini mengembalikan string label aktivitas
            return Response({"activity": predicted_label})
        except Exception as e:
            return Response({"error": str(e)}, status=500)