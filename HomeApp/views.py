import imp
from unicodedata import category
from django.shortcuts import render,HttpResponse
from EcomApp.models import product
# Create your views here.

def home(request):
    electronic_product = product.objects.filter(category='electronic gadgets')[0:4]
    fashion_product = product.objects.filter(category='fashion')[0:4]
    shoe_product = product.objects.filter(category='Shoe')[0:4]
    print(shoe_product)
    context = {'ep':electronic_product,'fp':fashion_product,'sp':shoe_product} 
    return render(request,'home.html',context)
    


