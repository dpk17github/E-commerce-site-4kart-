from django.urls import path,include
from . import views

urlpatterns = [
    path('<int>',views.shopshow,name='shopshow'),
    path('',views.shop,name='shop'),
]
