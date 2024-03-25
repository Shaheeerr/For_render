from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class CategorySerializer(serializers.ModelSerializer):    #category model
    
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):       #brand model serializer
    
    class Meta:
        model = Brand
        fields = ['name']

class SizeSerializer(serializers.ModelSerializer):         #size model serializer
    
    class Meta:
        model = Size
        fields = ['name']



class ProductVariantSerializer(serializers.ModelSerializer):        #Product Varient serializer
    
    class Meta:
        model = ProductVariant
        fields = ['variant_id','product','size','brand','price','img']



class ProductSerializer(serializers.ModelSerializer):       #Product model serializer
    variants = ProductVariantSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['description','name','category','variants']

class ProductImageSerializer(serializers.ModelSerializer):     #Product image serializer

    class Meta:
        model = ProductImage
        fields = ['img_id']





class CartItemSerializer(serializers.ModelSerializer):           #CartItem serializer
    product = ProductVariantSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = CartItem
        fields = ["id","cart","quantity","product","is_active","sub_total"]

    def total(self, cartitems:CartItem):         #subtotal for a single product item 
        return cartitems.quantity * cartitems.product.price



class CartSerializer(serializers.ModelSerializer):     #Cart Serializer
    id            = serializers.IntegerField(read_only=True) 
    user_name     = serializers.StringRelatedField(source='user.username', read_only=True)  # Use StringRelatedField to get the username  
    items         = CartItemSerializer(many=True,read_only=True)
    total_amount  = serializers.SerializerMethodField(method_name="main_total")   #main_total method to find the total of the cart


    class Meta:
        model    = Cart
        fields   = ["id","user","user_name","is_active","items","total_amount"]

    def main_total(self, cart:Cart):   # total amount in a cart
        items    = cart.items.all()
        total    = sum([item.quantity * item.product.price for item in items])    #sum function list comprehension
        return total

    







class AddtoCartSerializer(serializers.ModelSerializer):
    
    """serializer for add the cart"""

    product = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())  # Assuming ProductVariant is the related model
    
    def validate_variant_id(self, value):
        if not ProductVariant.objects.filter(variant_id=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        return value

    def save(self, **kwargs):
        cart_id    = self.context["cart_id"]
        product = self.validated_data["product"]
        quantity = self.validated_data["quantity"]
        
        
        try:
            cartitem = CartItem.objects.get(product=product, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()

            self.instance = cartitem

        except ObjectDoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)


        return self.instance

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "is_active"]



class CartUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)

    class Meta:
        model= CartItem
        fiels = ['id','quantity']
















