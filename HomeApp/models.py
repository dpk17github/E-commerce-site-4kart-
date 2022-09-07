from distutils.text_file import TextFile
from django.db import models
from  django.contrib.auth.models import User 
from EcomApp.models import cart,cartItems
# Create your models here.

class userAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userAddress')
    state = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    zip = models.IntegerField(default=0)

    def __str__(self):
        return self.state
        
    def cart_count(self):
        return cartItems.objects.filter(cart__is_paid =False, cart__user =self.user).count()
    
class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    product = models.TextField()
    amount = models.IntegerField(default=0)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    zip = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=100)
    payment_Status = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return f"order by {self.first_name}({self.user}) is [{self.product[1:20]}..etc] VIA {self.payment_method}"