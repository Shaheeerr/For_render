from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import CategorySerializer,BrandSerializer,SizeSerializer,ProductSerializer,ProductImageSerializer,ProductVariantSerializer,CartItemSerializer,CartSerializer,AddtoCartSerializer
from rest_framework.views import APIView
from rest_framework import generics, permissions, status, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin,ListModelMixin
from rest_framework.viewsets import GenericViewSet
from urllib import response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination






class CategoryViewSet(ModelViewSet): 

    """Catergory View"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer




class BrandViewSet(ModelViewSet):

    """BrandView"""

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class SizeViewSet(ModelViewSet):

    """Size View Set"""

    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class ProductViewSet(ModelViewSet):

    """ProductView"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]       # djangofilter for search,ordering,filter
    filterset_fields = ['category_id']
    search_fields = ['name','description']
    ordering_fields = ['name']
    pagination_class = PageNumberPagination



class ProductImageViewSet(ModelViewSet):

    """Product image View"""

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductVariantViewSet(ModelViewSet):

    """ProductVariantView"""

    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer




class CartViewSet(CreateModelMixin,ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):

    """Cart View Set."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


    def get_queryset(self):
        # Filter the queryset to only include the authenticated user's cart
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the newly created cart with the authenticated user
        serializer.save(user=self.request.user)







class CartItemViewSet(ModelViewSet):

    """Cart Item View"""
    
    def get_queryset(self):    # Overrides the get_queryset method of the viewset
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])   
     

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddtoCartSerializer
        
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        
        return CartItemSerializer

    def get_serializer_context(self):    # method ensures that the serializer has access to the cart_id from the URL pattern
        return {"cart_id": self.kwargs["cart_pk"]}
  













