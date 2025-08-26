from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SensorRecord, WeldingSession, PredictionResult, WelderProfile
from django.utils.timezone import now
from .serializers import SensorRecordSerializer
from .prediction_pipeline.predict import predict_latest_activity
from django.http import JsonResponse
from .session_manager import active_sessions


active_session = {}  # key: welder_id, value: WeldingSession

def dashboard_view(request):
    return render(request, 'dashboard/index.html')

class SensorRecordAPIView(APIView):
    def get(self, request, format=None):
        data = SensorRecord.objects.order_by('-timestamp')[:250]  # Ambil 250 data terakhir
        serializer = SensorRecordSerializer(data, many=True)
        return Response(serializer.data)
    
class ActivityPredictionAPIView(APIView):
    def get(self, request, format=None):
        welder_id = request.query_params.get("welder_id")  # ambil dari URL ?welder_id=1
        try:
            predicted_label = predict_latest_activity(welder_id=int(welder_id) if welder_id else None)
            return Response({"activity": predicted_label})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class StartSessionAPIView(APIView):
    def post(self, request):
        welder_id = request.data.get('welder_id')
        try:
            welder = WelderProfile.objects.get(id=welder_id)
            session = WeldingSession.objects.create(welder=welder, start_time=now())
            active_sessions[welder.id] = session  # simpan sesi aktif untuk welder ini
            return Response({"message": "Session started", "session_id": session.id})
        except WelderProfile.DoesNotExist:
            return Response({"error": "Welder not found"}, status=404)

class StopSessionAPIView(APIView):
    def post(self, request):
        session_id = request.data.get('session_id')
        try:
            session = WeldingSession.objects.get(id=session_id, end_time__isnull=True)
        except WeldingSession.DoesNotExist:
            return Response({"error": "No active session"}, status=400)

        session.end_time = now()
        session.save()
        if session.welder.id in active_sessions:
            active_sessions.pop(session.welder.id)
        return Response({"message": "Session stopped"})
    
class ActivityStatsAPIView(APIView):
    def get(self, request):
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response({"error": "Missing session_id"}, status=400)
        try:
            results = PredictionResult.objects.filter(session_id=session_id).order_by('created_at')
        except:
            return Response({"error": "Invalid session_id"}, status=400)
        if not results.exists():
            return Response({"error": "No predictions found for this session"}, status=404)

        # Hitung jumlah prediksi per label
        counts = {}
        for r in results:
            counts[r.predicted_class] = counts.get(r.predicted_class, 0) + 1

        # Buat urutan timeline untuk bar chart
        sequence = [
            {
                "label": r.predicted_class,
                "confidence": r.confidence,
                "timestamp": r.created_at.isoformat()
            } for r in results
        ]

        return Response({
            "counts": counts,
            "sequence": sequence
        })

