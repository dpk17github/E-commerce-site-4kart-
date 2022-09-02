import imp
from itertools import count
from unicodedata import category
from django.shortcuts import render,HttpResponse,redirect
from EcomApp.models import product,cart,cartItems
from HomeApp.models import userAddress
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q
# Create your views here.

def home(request):
    electronic_product = product.objects.filter(category__icontains='electronic gadgets')[0:4:-1]
    fashion_product = product.objects.filter(category__icontains='fashion')[0:4:-1]
    shoe_product = product.objects.filter(category__icontains='Shoe')[0:4]
    context = {'ep':electronic_product,'fp':fashion_product,'sp':shoe_product} 
    user = request.user
    if user.id == None:
        pass
    else:
        userdata = userAddress.objects.filter(user=request.user).first()
        context.update({'u':userdata})
    return render(request,'home.html',context)
    
    
def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        filter = request.POST.get('filter')
        print(filter)
        if filter == 'nf':
            fs= product.objects.filter( Q(category__icontains='fashion') , Q(search_key__icontains = search))
            context ={'allpro':fs}
            total = fs.count()
            messages.warning(request,f'We have {total} Search Result for {search}')
            return render(request,'search.html',context)
        if filter == 'mf':
            fs= product.objects.filter( Q(category__icontains='fashion'), Q(search_key__icontains = search), Q(for_gender='M'))
            context ={'allpro':fs}
            total = fs.count()
            messages.warning(request,f'We have {total} Search Result for {search}')
            return render(request,'search.html',context)
        if filter == 'wf':
            fs= product.objects.filter( Q(category__icontains='fashion'), Q(search_key__icontains = search), Q(for_gender='F'))
            context ={'allpro':fs}
            total = fs.count()
            messages.warning(request,f'We have {total} Search Result for {search}')
            return render(request,'search.html',context)
        if filter == 'gadgets':
            fs= product.objects.filter( Q(category__icontains='electronic gadgets'), Q(search_key__icontains = search))
            context ={'allpro':fs}
            total = fs.count()
            messages.warning(request,f'We have {total} Search Result for {search}')
            return render(request,'search.html',context)
        if filter == 'all':
            bycat = product.objects.filter(category__icontains= search)
            byname = product.objects.filter(search_key__icontains = search)
            pro = bycat.union(byname)
            total = bycat.union(byname).count()
            context ={'allpro':pro,'search':search,}
            messages.warning(request,f'We have {total} Search Result for {search}')
        user = request.user
        if user.id == None:
            pass
        else:
            userdata = userAddress.objects.filter(user=request.user).first()
            context.update({'u':userdata})
        return render(request,'search.html',context)

    return HttpResponse('404 page not found')


def signup(request):
    if request.method =="POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(first_name,last_name,username,email,phone,password1,password2)
        if len(first_name) < 3:
            messages.error(request,'Sorry! Sign up fail.. Your first name should be more than 3 chractor')
            return redirect('/signup')
        if len(last_name) < 3:
            messages.error(request,'Sorry! Sign up fail.. Your last name should be more than 3 chractor')
            return redirect('/signup')
        if len(username) < 3:
            messages.error(request,'Sorry! Sign up fail.. Username should be more than 3 chractor')
            return redirect('/signup')
        if not username.isalnum():
            messages.error(request,'Sorry! Sign up fail.. Username should contain letters or numbers only')
            return redirect('/signup')
        if len(email) < 10:
            messages.error(request,'Sorry! Sign up fail.. Please enter valid email address')
            return redirect('/signup')
        if len(phone) < 10:
            messages.error(request,'Sorry! Sign up fail.. Pleaase enter valid Phone number')
            return redirect('/signup')
        if len(password1) < 8:
            messages.error(request,'Sorry! Sign up fail.. Password should be more than 8 chractor')
            return redirect('/signup')
        if password1 != password2:
            messages.error(request,'Sorry! Sign up fail.. Password do not match')
            return redirect('/signup')
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.city = last_name
        myuser.save()
        messages.success(request,"Your 4kart Account has been create Successfully")
        return redirect('/signup')
    return render(request,'signup.html')
    

def loginpage(request):
    return render(request,'login.html')


def handlelogin(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully login')
            return redirect('/')
        else:
            messages.error(request,'login fail.. invalid credentials, Try Again!')
            return redirect('/loginpage')
    return HttpResponse('404 page not found')

def handlelogout(request):
    logout(request)
    messages.success(request,'logout succesfully')
    return redirect('/')

def profile(request):
    if request.method =='POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        zip = request.POST.get('zip')
        userid = request.POST.get('userid')
        check = request.POST.get('check','off')
        if check == 'on':
            print(first_name,last_name,email,username,state,city,address,zip,userid,check)
            myuser = User.objects.get(id=userid)
            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.email = email
            myuser.username = username
            myuser.save()

            useraddress =userAddress(id=userid,user_id=userid,state=state,city=city,address=address,zip=zip)
            useraddress.save()
            messages.success(request,'Profile updated successfully')
            return redirect('/profile')
        else:
            messages.error(request,'Profile updated fail.. make sure before submit ')
            return redirect('/profile')
    userdata = userAddress.objects.filter(user=request.user).first()
    print(userdata)
    context = {'u':userdata}
    return render(request,'profile.html',context)
    
def viewcart(request):
    allcart = cartItems.objects.filter(cart=request.user.id)
    print(allcart)
    totalprice = 0
    for item in allcart:
        totalprice =totalprice + item.product.price
    context={'allcart':allcart,'totalprice':totalprice}
    user = request.user
    if user.id == None:
        pass
    else:
        userdata = userAddress.objects.filter(user=request.user).first()
        context.update({'u':userdata})
    return render(request,'cart.html',context)

def remove_cart(request, int):
    rm = cartItems.objects.get(id = int)
    thisproduct = rm.product
    rm.delete()
    messages.warning(request,f'{thisproduct} Has Been Remover from Cart')
    return redirect('/viewcart')
