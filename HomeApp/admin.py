from django.contrib import admin

from HomeApp.models import userAddress
from .models import userAddress,order
# Register your models here.
admin.site.register((userAddress,order))