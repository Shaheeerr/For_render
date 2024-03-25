from django.urls import path 
from .views import *
from rest_framework.routers import DefaultRouter   # import default router
from rest_framework_nested import routers   # import router
from . import views


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'size', SizeViewSet, basename='size')




cart_router = routers.NestedDefaultRouter(router, 'cart', lookup="cart")     #nested router for cart
cart_router.register("items", views.CartItemViewSet, basename='cart-items')



urlpatterns = router.urls + cart_router.urls

