from rest_framework import serializers
from .models import *
from home.models import *
from django.db import transaction
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from register.models import Address



class OrderItemSerializer(serializers.ModelSerializer):  #serializer for order item
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):    #serializer for Order
    order_items = OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'shipping_address', 'status','order_items']




class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'




class CreateOrderSerilizer(serializers.Serializer):       #serializer for Create a Order
    cart_id = serializers.CharField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():    #check the cart_id 
            raise serializers.ValidationError("This cart_id is invalid")                    

        elif not CartItem.objects.filter(cart_id=cart_id).exists():    # check the cart is empty or not
            raise serializers.ValidationError("Sorry your cart is empty")
        
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():          # add atomic in Acid Property
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            order = Order.objects.create(customer_id = user_id)  
            
            # Save the current state to the historical records
            
            action = f"Order created by user_id {user_id}"
            HistoricalRecord.objects.create(action=action,user_id=user_id)
            
            cartitems = CartItem.objects.filter(cart_id=cart_id)  
            orderitems = [
                OrderItem(order=order, 
                    product=item.product, 
                    quantity=item.quantity
                    )
            for item in cartitems
            ]
            OrderItem.objects.bulk_create(orderitems)
            CartItem.objects.filter(cart_id=cart_id).delete()

        return order





class UpdateOrderSerializer(serializers.ModelSerializer): #serilizer for update serializer
    class Meta:
        model = Order 
        fields = ["pending_status"]




















    




