from rest_framework import serializers
from .models import Service, CheckResult

class CheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckResult
        fields = ['id', 'status', 'response_time_ms', 'checked_at']

class ServiceSerializer(serializers.ModelSerializer):
    check_results = CheckResultSerializer(many = True, read_only=True)
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'url', 'check_interval_minutes', 'grace_period_minutes', 'is_active', 'created_at', 'check_results'
            ]
        read_only_fields=['owner']