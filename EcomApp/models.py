from ast import Delete
from distutils.text_file import TextFile
from operator import truediv
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from unicodedata import category
from django.db import models
from  django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here

GENDER_CHOICES = (
   ('M', 'Male'),
   ('F', 'Female')
)

     

class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    price_off = models.IntegerField(default=0, blank=True)
    color = models.CharField(max_length=50)
    search_key = models.TextField()
    size = models.CharField(max_length=50, blank=True)
    for_gender = models.CharField(choices=GENDER_CHOICES, max_length=128)
    des = models.CharField(max_length=300)
    img =models.ImageField(upload_to="static/img",default="")

    def __str__(self):
        return self.product_name


class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

class cartItems(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE,related_name="cart_items")
    product = models.ForeignKey(product, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return f"{self.product} by {self.cart}"



class Post_reviews(models.Model):
    review = models.CharField(max_length=500)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField(default=now)

    def __str__(self):
        return self.review