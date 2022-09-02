from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('profile',views.profile,name='profile'),
    path('handlelogin',views.handlelogin,name='handlelogin'),
    path('handlelogout',views.handlelogout,name='handlelogout'),
    path('loginpage',views.loginpage,name='loginpage'),
    path('signup',views.signup,name='signup'),
    path('viewcart',views.viewcart,name='viewcart'),
    path('remove_cart/<int>',views.remove_cart,name='remove_cart'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
