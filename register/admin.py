from django.contrib import admin
from .models import CustomUser,Address


@admin.register(CustomUser) #admin decarator
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['id','email','username','created_at','is_staff']

admin.site.register(Address)


