from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SensorRecord
from .serializers import SensorRecordSerializer

def dashboard_view(request):
    return render(request, 'dashboard/index.html')

class SensorRecordAPIView(APIView):
    def get(self, request, format=None):
        data = SensorRecord.objects.order_by('-timestamp')[:250]  # Ambil 250 data terakhir
        serializer = SensorRecordSerializer(data, many=True)
        return Response(serializer.data)