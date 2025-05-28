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
