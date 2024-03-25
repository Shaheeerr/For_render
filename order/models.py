from django.db import models
from register.models import CustomUser,Address
import uuid
from django.utils.functional import cached_property
from home.models import ProductVariant
from django.utils.translation import gettext_lazy as _
# from djangoaudit.models import AuditedModel
from django.utils import timezone



class HistoricalRecord(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=255)
    user_id = models.IntegerField(null=True, blank=True)
    # Add more fields as needed to capture information about the change

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} at {self.timestamp}"





class Order(models.Model):        # Order Model

    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]


    PAYMENT_COD = "COD"
    PAYMENT_RAZOR_PAY = "RAZOR PAY"

    PAYMENT_CHOICES = [
        (PAYMENT_COD, "Cash On Delivery"),
        (PAYMENT_RAZOR_PAY, "FLUTTER PAY Payment")
    ]


    id          = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer    = models.ForeignKey('register.CustomUser', on_delete=models.CASCADE, related_name='orders',null=True,blank=True)
    status      = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    payment     = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default=PAYMENT_COD)

    shipping_address = models.ForeignKey(
        Address,
        related_name="shipping_orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)




    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.customer.username

    @property
    def total_price(self):
        items = self.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total
    



class OrderItem(models.Model):     # Order Item Model

    # """A dummy model to test the functionality of the AuditedModel"""

    # log_fields = ('order', 'product', 'quantity', 'created_at', 'updated_at')


    order       = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product     = models.ForeignKey(ProductVariant, related_name="product_orders", on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    


    class Meta:
        ordering = ("-created_at",)
    



