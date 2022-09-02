from django.contrib import admin
from EcomApp.models import product,Post_reviews,cart,cartItems
# Register your models here.
admin.site.register(product)
admin.site.register(Post_reviews)
admin.site.register(cart)
admin.site.register(cartItems)