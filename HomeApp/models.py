from django.db import models
from  django.contrib.auth.models import User 
from EcomApp.models import cart,cartItems
# Create your models here.

class userAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userAddress')
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    zip = models.IntegerField(default=0)

    def __str__(self):
        return self.state
        
    def cart_count(self):
        return cartItems.objects.filter(cart__is_paid =False, cart__user =self.user).count()
    