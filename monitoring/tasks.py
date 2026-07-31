import time
import requests
from celery import shared_task
from django.utils import timezone
from .models import Service, CheckResult

@shared_task
def check_service(service_id):
    try:
        service = Service.objects.get(id =service_id, is_active = True)
    except Service .DoesNotExist:
        return

    start = time.time()
    try:
        response = requests.get(service.url, timeout=10)
        elapsed_ms = int((time.time() - start) * 1000)
        status = 'up' if response.status_code < 400 else 'down'
    except requests.RequestException:
        elapsed_ms = None
        status = 'down'


    CheckResult.objects.create(
        service = service,
        status = status,
        response_time_ms=elapsed_ms
    )        


@shared_task
def check_all_active_services():
    for service in Service.objects.filter(is_active=True):
        check_service.delay(service.id)
            

