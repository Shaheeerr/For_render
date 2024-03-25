from django.contrib import admin
from .models import *


@admin.register(Order)  # admin register for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'payment')



@admin.register(OrderItem)   # admin register for OrderItem
class OrderItemAdmin(admin.ModelAdmin): 
    list_display = ('id', 'order', 'product', 'quantity')


@admin.register(HistoricalRecord)   # admin register for HistoricalRecord
class OrderItemAdmin(admin.ModelAdmin): 
    list_display = ('timestamp', 'action')
