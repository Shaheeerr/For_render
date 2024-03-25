from django.urls import path, include
from .views import OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Register the OrderViewSet with the router
router.register(r'orders', OrderViewSet, basename='orders')


urlpatterns = router.urls


