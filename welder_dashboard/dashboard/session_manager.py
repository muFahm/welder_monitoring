# dashboard/session_manager.py
from .models import WeldingSession

active_sessions = {}  # key: welder_id (int), value: WeldingSession instance

def initialize_active_sessions():
    global active_sessions
    sessions = WeldingSession.objects.filter(end_time__isnull=True)
    for session in sessions:
        active_sessions[session.welder.id] = session
    print(f"[INFO] Initialized active_sessions: {active_sessions}")