from django.urls import path,include
from . import views

urlpatterns = [
    path('review',views.review,name='review'),
    path('add-to-cart/<int>',views.add_to_cart,name='add_to_cart'),
    path('<int>',views.shopshow,name='shopshow'),
    path('',views.shop,name='shop'),
]
