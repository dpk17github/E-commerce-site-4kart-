from distutils.text_file import TextFile
from statistics import mode
from unicodedata import category
from django.db import models

# Create your models here.

class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    price_off = models.IntegerField(default=0, blank=True)
    size = models.CharField(max_length=50, blank=True)
    des = models.CharField(max_length=300)
    img =models.ImageField(upload_to="static/img",default="")

    def __str__(self):
        return self.product_name
