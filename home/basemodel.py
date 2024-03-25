from django.db import models
from django.utils import timezone   # import timezone
from django.utils.text import slugify  # import slugyfy



class BaseModel(models.Model):    

    """Base class for all models in the application."""

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
