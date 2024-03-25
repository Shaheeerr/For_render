from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

class ProductVariantInline(admin.StackedInline):   #set StackedInline for ProductVariantInline
    model = ProductVariant
    extra = 1 

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]     #inline the ProductVarient

admin.site.register(Product, ProductAdmin)    

@admin.register(Category,ProductVariant,CartItem)   #register with admin.site register
class MyModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)                                 # register for brand
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')

@admin.register(Size)                                   # register for size
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')

@admin.register(Cart)                                   # register for cart 
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_active')

