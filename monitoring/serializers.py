from rest_framework import serializers
from .models import Service, CheckResult
import ipaddress
from urllib.parse import urlparse
import socket

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


    def validate_url(self,value):
        hostname = urlparse(value).hostname
        try:
            ip = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.is_private or ip_obj.is_loopback:
                raise serializers.ValidationError("Private/internal URLs are not allowed.")
        except socket.gaierror:
            raise serializers.ValidationError("Could not resolve hostname.")
        return value