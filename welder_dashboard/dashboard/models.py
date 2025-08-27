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
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    
    certification_id = models.CharField(max_length=100, unique=True)
    certification_body = models.CharField(max_length=100, blank=True, help_text="Lembaga penerbit sertifikasi")
    certification_expiry = models.DateField(null=True, blank=True)

    experience_years = models.IntegerField(default=0)
    skills = models.TextField(blank=True, help_text="Jenis pengelasan yang dikuasai, misal: SMAW, TIG, MIG")

    profile_photo = models.ImageField(upload_to='welder_photos/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.certification_id}"

class PredictionResult(models.Model):
    predicted_class = models.CharField(max_length=100)  # misal: "arc_start", "steady_weld"
    confidence = models.FloatField()
    window_start = models.DateTimeField()
    window_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_class} ({self.confidence:.2f})"
