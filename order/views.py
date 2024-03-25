from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from home.models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
import requests
import uuid
from django.conf import settings
import json
import logging


logger = logging.getLogger(__name__)


def initiate_payment(amount,email,order_id):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {settings.FLW_SEC_KEY}"  # Replace with your actual FLW_SECRET_KEY
    }
    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "NGN",
        "redirect_url": f"http://127.0.0.1:8000/home/confirm_payment/?o_id={order_id}",
        "meta": {
            "consumer_id": 23,
            "consumer_mac": "92a3-912ba-1192a"
        },
        "customer": {
            "email": email,
            "phonenumber": "080****4528",
            "name": "Yemi Desola"
        },
        "customizations": {
            "title": "Pied Piper Payments",
            "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        # response.raise_for_status()  # Raise an exception for HTTP errors
        # response_data = response.json()
        return Response(response.json())

    except requests.exceptions.RequestException as err:
        logger.error(f"The payment request failed: {err}")
        logger.error(f"Response content: {response.content}")
        return Response({"error": str(err)},status=500)






class OrderViewSet(ModelViewSet):   # Get User Order
    
    http_method_names = ["get", "patch", "post", "delete", "options", "head"]
    
    @action(detail=True, methods=['POST'])
    def pay(self, request, pk):
        order = self.get_object()
        amount = order.total_price
        email = request.user.email
        order_id = str(order.id)
        # redirect_url = "http://127.0.0.1:8000/home/orders/confirm"
        return initiate_payment(amount, email, order_id)


    @action(detail=False, methods=["POST"])
    def confirm_payment(self, request):
        order_id = request.GET.get("o_id")
        order = Order.objects.get(id=order_id)
        order.status = "C"
        order.save()
        serializer = OrderSerializer(order)

        data = {
            "msg":"payment is successfull",
            "data" : serializer.data
        }
        return Response(data)

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get_permissions(self):
        if self.request.method.lower() in ["patch", "delete"]:  # Convert to lowercase for proper comparison
            return [IsAdminUser()]
        return [IsAuthenticated()]                         # else , only authenticated users can access the data
    
    
    
    def create(self, request, *args, **kwargs):             # create method
        serializer = CreateOrderSerilizer(data=request.data, context={"user_id": self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    
    def get_serializer_class(self):
        if self.request.method == 'POST':    # if request is POST  then use create Serializer class
            return CreateOrderSerilizer  
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer   
        return OrderSerializer
        
    
    def get_queryset(self):                    # get querymethod
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()       
        return Order.objects.filter(customer=user)
    
    

    
    
    
    
    
    












    # serializer_class = OrderSerializer
    # queryset=Order.objects.all()
    # permission_classes = [IsAuthenticated]  # This ensures that only authenticated users can access this view
    # authentication_classes = [JWTAuthentication]


    # def get_serializer_class(self):
    #     if self.request.method=="POST":
    #         return CreateOrderSerilizer
    #     return OrderSerializer

    # def get_queryset(self):
    #     # Only return orders related to the authenticated user
    #     return Order.objects.filter(customer=self.request.user)


