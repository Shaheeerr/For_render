from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect,render
from django.utils import timezone
from django_countries.fields import CountryField




class CustomUserManager(BaseUserManager):  #inherit BaseuserManager
    def create_user(self, username, email, password=None, **extra_fields):  # usermanager for create user
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  #normalize the email
        user = self.model(username=username, email=email, **extra_fields)  #save the fields into user
        user.set_password(password)   # hash the password
        user.save(using=self._db)
        return user 

    def create_superuser(self, username, email, password=None, **extra_fields):   # usermanager for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):  # inherit AbstaractBase, PermissionMixin
    id              = models.AutoField(primary_key=True)    # primary key
    username        = models.CharField(max_length=80)
    otp             = models.CharField(max_length=6)
    otp_time        = models.DateTimeField(blank=True, null=True)
    is_verified     = models.BooleanField(default=False)
    email           = models.EmailField(unique=True)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    password        = models.CharField(max_length=128)
    created_at      = models.DateTimeField(_('Created At'), auto_now_add=True)  # created date
    profile_picture = models.ImageField(_('Profile Picture'), upload_to='profile_pics/', blank=True, null=True)


    USERNAME_FIELD = 'email'  # add email field into UsernameField
    REQUIRED_FIELDS = ['username']  # add email field into REQUIRED_FIELDS

    objects = CustomUserManager()  #add customeruser into a object

    def __str__(self):
        return self.username   # username is see in the database
        



class Address(models.Model):
    # Address options
    BILLING = "B"
    SHIPPING = "S"

    ADDRESS_CHOICES   = ((BILLING, _("billing")), (SHIPPING, _("shipping")))

    user              = models.ForeignKey(CustomUser, related_name="addresses", on_delete=models.CASCADE) # connect with the CustomUser
    default           = models.BooleanField(default=False)
    country           = CountryField()
    city              = models.CharField(max_length=100)
    street_address    = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code       = models.CharField(max_length=20, blank=True)

    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
    
    def __str__(self):
        return str(self.user.username)  # see the username who is it


















