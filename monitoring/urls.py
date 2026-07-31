from rest_framework .routers import DefaultRouter
from .views import ServiceViewSet, CheckResultViewSet

router = DefaultRouter()
router.register('services', ServiceViewSet, basename ='service')
router.register('check -results', CheckResultViewSet, basename='checkresult')

urlpatterns = router.urls
