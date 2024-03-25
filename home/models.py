from django.db import models
from mptt.models import MPTTModel, TreeForeignKey   # import MPTTModel and TreeForeignkey for  hierarchical
from django.utils.text import slugify
from .basemodel import BaseModel
from django_model_history_tracker.mixins import HistoryTrackerMixin



class Category(MPTTModel): #inherit MPTTModel
    name      =models.CharField(max_length=50,unique=True)
    parent    = TreeForeignKey("self", on_delete=models.PROTECT, null=True,blank=True) # implement tree foreignkey
    slug      = models.SlugField(max_length=200,unique=True,null=True,blank=True)


    class MPTTMeta:
        order_insertion_by = ['name'] #ordered by its name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Brand(BaseModel): # Brand model table
    name=models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class Size(models.Model,HistoryTrackerMixin):   # size model table
    name = models.CharField(max_length=50,default='',unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Product(BaseModel):  # product model table
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)    # foreignkey with Category
    img   = models.ImageField(upload_to='product/',blank=True,null=True)
    is_active   = models.BooleanField(default=False)

    def _str_(self) -> str:
        return self.name


class ProductImage(models.Model): #product image table
    img_id    = models.CharField(max_length=200,null=True)
    img_1     = models.ImageField(upload_to="prdv1/",null=True,blank=True)
    img_2     = models.ImageField(upload_to="prdv2/",null=True,blank=True)
    img_3     = models.ImageField(upload_to="prdv3/" ,null=True,blank=True)

    def _str_(self) -> str:
        return f"{self.img_id}"




class ProductVariant(BaseModel):  # product Varient Table
    variant_id  = models.AutoField(primary_key=True, unique=True,default=None)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='variants')
    size        = models.ForeignKey(Size, on_delete=models.CASCADE,null=True)
    brand       = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField()
    slug        = models.SlugField(max_length=200,unique=True,null=True,blank=True)
    img         = models.ForeignKey(ProductImage,on_delete=models.CASCADE,default=None,blank=True,null=True)
    is_active   = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product.name)
        super(ProductVariant, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return f"{self.variant_id}" 



class CartItem(models.Model):  # Cart Item Model
    cart      = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name="items")    # FK to Cart
    product   = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)     #Fk to ProductVarient
    quantity  = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return str(self.cart)


class Cart(models.Model):  #Cart model table
    id            = models.AutoField(primary_key=True)
    user          = models.OneToOneField("register.CustomUser", on_delete=models.CASCADE, unique=True)  #oneToOne  Field
    cart_items    = models.ManyToManyField(ProductVariant, through='CartItem')    #ManytoMany Field
    is_active     = models.BooleanField(default=False)


    def __str__(self):
        return f"Cart for {self.user.username}"




 