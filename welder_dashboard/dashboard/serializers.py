# welder_dashboard/dashboard/serializers.py
from rest_framework import serializers
from .models import SensorRecord, WelderProfile

class SensorRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorRecord
        fields = [
            "id", "timestamp",
            "ax", "ay", "az",
            "gx", "gy", "gz",
            "mx", "my", "mz"
        ]


class WelderProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    experience = serializers.IntegerField(source="experience_years")
    skills = serializers.SerializerMethodField()

    class Meta:
        model = WelderProfile
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "certification_id",
            "certification_body",
            "certification_expiry",
            "experience",
            "skills",
            "photo_url",
        ]

    def get_photo_url(self, obj):
        if obj.profile_photo:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.profile_photo.url) if request else obj.profile_photo.url
        return None

    def get_skills(self, obj):
        if not obj.skills:
            return []
        return [s.strip() for s in obj.skills.split(",")]