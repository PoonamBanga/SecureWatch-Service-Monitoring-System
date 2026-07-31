from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Service, CheckResult
from .serializers import ServiceSerializer, CheckResultSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CheckResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CheckResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CheckResult.objects.filter(services__owner=self.request.user)

    