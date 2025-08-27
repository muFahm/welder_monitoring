from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SensorRecord, PredictionResult, WelderProfile
from django.utils.timezone import now
from .serializers import SensorRecordSerializer, WelderProfileSerializer
from .prediction_pipeline.predict import predict_latest_activity
from django.http import JsonResponse

def dashboard_view(request):
    return render(request, 'dashboard/index.html')

class WelderProfileAPIView(APIView):
    def get(self, request, welder_id=None):
        if welder_id:
            try:
                welder = WelderProfile.objects.get(id=welder_id)
                serializer = WelderProfileSerializer(welder, context={'request': request})
                return Response(serializer.data)
            except WelderProfile.DoesNotExist:
                return Response({"error": "Welder not found"}, status=404)
        else:
            # kalau tidak ada welder_id, return semua welder
            welders = WelderProfile.objects.all()
            serializer = WelderProfileSerializer(welders, many=True, context={'request': request})
            return Response(serializer.data)

class SensorRecordAPIView(APIView):
    def get(self, request, format=None):
        results = PredictionResult.objects.order_by('-created_at')[:50]
        if not results.exists():
            return Response([])

        total = results.count()
        data = []
        for r in results:
            data.append({
                "class": r.predicted_class.lower(),
                "width": 100 / total
            })

        return Response(data)
    
class LatestSensorAPIView(APIView):
    def get(self, request, format=None):
        latest = SensorRecord.objects.order_by('-timestamp').first()
        if not latest:
            return Response({"error": "No sensor data"}, status=404)

        return Response({
            "timestamp": latest.timestamp.isoformat(),
            "ax": latest.ax, "ay": latest.ay, "az": latest.az,
            "gx": latest.gx, "gy": latest.gy, "gz": latest.gz,
            "mx": latest.mx, "my": latest.my, "mz": latest.mz,
        })
    
class ActivityPredictionAPIView(APIView):
    def get(self, request, format=None):
        welder_id = request.query_params.get("welder_id")  # ambil dari URL ?welder_id=1
        try:
            result = predict_latest_activity(welder_id=int(welder_id) if welder_id else None)
            if isinstance(result, str):
                return Response({
                    "predicted_class": result,
                    "confidence": 1.0  # default kalau tidak ada skor
                })

            # kalau sudah dict dengan predicted_class & confidence
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
class ActivityStatsAPIView(APIView):
    def get(self, request):
        # Ambil semua hasil prediksi
        results = PredictionResult.objects.all()

        if not results.exists():
            return Response({"error": "No predictions found"}, status=404)

        # Hitung jumlah prediksi per label
        counts = {}
        for r in results:
            counts[r.predicted_class] = counts.get(r.predicted_class, 0) + 1

        return Response(counts)
