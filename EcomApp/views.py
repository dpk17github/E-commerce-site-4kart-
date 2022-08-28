from django.shortcuts import render,HttpResponse
from EcomApp.models import product
# Create your views here.


def shop(request):
    allpro = product.objects.all()
    context = {'allpro':allpro}
    return render(request,'shop.html',context)


def shopshow(request, int):
    pro = product.objects.filter(product_id=int).first()
    print(pro)
    context = {'pro':pro}
    return render(request,'shopshow.html',context)