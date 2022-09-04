import http
from django.shortcuts import render,HttpResponse,redirect
from EcomApp.models import product,Post_reviews,cart,cartItems
from HomeApp.models import userAddress
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


def shop(request):
    allpro = product.objects.all()
    context = {'allpro':allpro}
    user = request.user
    if user.id == None:
        pass
    else:
        userdata = userAddress.objects.filter(user=request.user).first()
        context.update({'u':userdata})
    return render(request,'shop.html',context)


def shopshow(request, int):
    pro = product.objects.filter(product_id=int).first()
    review = Post_reviews.objects.filter(product=pro)
    context = {'pro':pro,'reviews':review,}
    user = request.user
    if user.id == None:
        pass
    else:
        userdata = userAddress.objects.filter(user=request.user).first()
        context.update({'u':userdata})
    return render(request,'shopshow.html',context)

def add_to_cart(request, int):
    user = request.user
    userproduct = product.objects.get(product_id = int)

    create_cart , _ = cart.objects.get_or_create(user = user, is_paid = False)

    add_in_cart = cartItems.objects.create(cart = create_cart, product = userproduct)
    add_in_cart.save()
    messages.success(request,f'{userproduct} added successfully in your cart')
    return redirect('/shop')


def review(request):
    if request.method =='POST':
        review = request.POST.get('review')
        productid = request.POST.get('proid')
        pro = product.objects.get(product_id=productid)
        user = request.user
        print(review,productid,user,pro)
        add_review = Post_reviews(review=review,product=pro,user=user)
        add_review.save()
        return redirect(f'/shop/{productid}')
    return HttpResponse('error 404 page not found')
    