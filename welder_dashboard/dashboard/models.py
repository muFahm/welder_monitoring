from django.db import models

class SensorRecord(models.Model):
    ax = models.FloatField()
    ay = models.FloatField()
    az = models.FloatField()
    
    gx = models.IntegerField()
    gy = models.IntegerField()
    gz = models.IntegerField()
    
    mx = models.FloatField()
    my = models.FloatField()
    mz = models.FloatField()
    
    timestamp = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"SensorRecord at {self.timestamp}"

class WelderProfile(models.Model):
    name = models.CharField(max_length=100)
    certification_id = models.CharField(max_length=100, unique=True)
    experience_years = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.certification_id}"

class WeldingSession(models.Model):
    welder = models.ForeignKey(WelderProfile, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"Session {self.id} by {self.welder.name} on {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"

class PredictionResult(models.Model):
    session = models.ForeignKey(WeldingSession, on_delete=models.CASCADE)
    predicted_class = models.CharField(max_length=100)  # misal: "arc_start", "steady_weld"
    confidence = models.FloatField()
    window_start = models.DateTimeField()
    window_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_class} ({self.confidence:.2f})"