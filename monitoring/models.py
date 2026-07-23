from django.db import models
from django.conf import settings

class Service(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services'
    )
    name = models.CharField(max_length=100)
    url = models.URLField()
    check_interval_minutes = models.PositiveIntegerField(default=5)
    grace_period_minutes = models.PositiveIntegerField(default =2)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):

        return f"{self.name} ({self.url})"


class CheckResult(models.Model):
    STATUS_CHOICES = (
        ('up', 'Up'),

        ('down', 'Down'),
    )    
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='check_results'
    )
    status = models.CharField(max_length=10, choices = STATUS_CHOICES)
    response_time_ms = models.PositiveIntegerField(null = True, blank = True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} - {self.status} @ {self.checked_at}"
    
