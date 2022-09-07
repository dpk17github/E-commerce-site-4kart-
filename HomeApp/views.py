import imp
from itertools import count
from pickle import NONE
from unicodedata import category
from django.shortcuts import render,HttpResponse,redirect
from EcomApp.models import product,cart,cartItems
from HomeApp.models import userAddress,order
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from payTm import checksum
MARCHANT_KEY = '9wAdaml3#7w3MGch';
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
        if search == '':
            search = 'empty value'
        filter = request.POST.get('filter')
        if filter == 'nf':
            fs= product.objects.filter( Q(category__icontains='fashion') , Q(search_key__icontains = search))
            context ={'allpro':fs}
            total = fs.count()
            messages.warning(request,f'We have {total} Search Result for {search}')
        if filter == 'mf':
            fs= product.objects.filter( Q(category__icontains='fashion'), Q(search_key__icontains = search), Q(for_gender='M'))
            context ={'allpro':fs}
            total = fs.count()
            messages.warning(request,f'We have {total} Search Result for {search}')
        if filter == 'wf':
            fs= product.objects.filter( Q(category__icontains='fashion'), Q(search_key__icontains = search), Q(for_gender='F'))
            context ={'allpro':fs}
            total = fs.count()
            messages.warning(request,f'We have {total} Search Result for {search}')
        if filter == 'gadgets':
            fs= product.objects.filter( Q(category__icontains='electronic gadgets'), Q(search_key__icontains = search))
            context ={'allpro':fs}
            total = fs.count()
            messages.warning(request,f'We have {total} Search Result for {search}')
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
        phone = request.POST.get('phone')
        zip = request.POST.get('zip')
        userid = request.POST.get('userid')
        check = request.POST.get('check','off')
        if check == 'on':
            myuser = User.objects.get(id=userid)
            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.email = email
            myuser.username = username
            myuser.save()

            useraddress =userAddress(id=userid,user_id=userid,state=state,city=city,address=address,phone=phone,zip=zip)
            useraddress.save()
            messages.success(request,'Profile updated successfully')
            return redirect('/profile')
        else:
            messages.error(request,'Profile updated fail.. make sure before submit ')
            return redirect('/profile')
    userdata = userAddress.objects.filter(user=request.user).first()
    context = {'u':userdata}
    return render(request,'profile.html',context)
    
def viewcart(request):
    allcart = cartItems.objects.filter(cart=request.user.id)
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

def checkbuy(request):
    allcart = cartItems.objects.filter(cart=request.user.id)
    totalprice = 0
    for item in allcart:
        totalprice =totalprice + item.product.price
    userdata = userAddress.objects.filter(user=request.user).first()
    cart = ''
    for cartitem in allcart:
        cart = cart + '*' + str(cartitem.product.product_name) + '\n'
    context={'allcart':allcart,'totalprice':totalprice,'u':userdata, 'cart':cart}
    return render(request,'buynow.html',context)

def checkbuy2(request,int):
    allcart = product.objects.filter(product_id = int)
    totalprice = 0
    for item in allcart:
        totalprice =totalprice + item.price
    userdata = userAddress.objects.filter(user=request.user).first()
    perticular = allcart.first()
    cart = perticular.product_name
    context={'allcart':allcart,'totalprice':totalprice,'u':userdata, 'cart':cart}
    return render(request,'buynow2.html',context)


def myorder(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        pro = request.POST.get('allproduct')
        email = request.POST.get('email')
        username = request.POST.get('user')
        phone = request.POST.get('phone')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        zip = request.POST.get('zip')
        amount = request.POST.get('amount')
        check = request.POST.get('check','off')
        radio = request.POST.get('exampleRadios','off')
        buyer = User.objects.get(id=username)
        if check == 'on':
            if radio == 'payTM':
                myorder = order(user=request.user,product=pro,first_name=first_name,last_name=last_name,email=email,phone=phone,
                state=state,city=city,address=address,zip=zip,amount=amount,payment_method=radio)
                myorder.save()
                param_dict={
                            'MID':'FDxrCj49984261690146',
                            'ORDER_ID': str(myorder.id),
                            'TXN_AMOUNT': str(amount),
                            'CUST_ID': email,
                            'INDUSTRY_TYPE_ID': 'Retail',
                            'WEBSITE': 'WEBSTAGING',
                            'CHANNEL_ID': 'WEB',
                            'CALLBACK_URL':'http://127.0.0.1:8000/handlepayment',
                            }
                param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MARCHANT_KEY)
                return  render(request, 'paytm.html', {'param_dict': param_dict})

            elif radio == 'Dcard':
                myorder = order(user=buyer,product=pro,first_name=first_name,last_name=last_name,email=email,phone=phone,
                state=state,city=city,address=address,zip=zip,amount=amount,payment_method=radio)
                # myorder.save()
                return HttpResponse(f'this service is temprary off please try another payment method<br> <h3><a href="/checkbuy">try another way!</a></h3>')
            elif radio == 'Ccard':
                myorder = order(user=buyer,product=pro,first_name=first_name,last_name=last_name,email=email,phone=phone,
                state=state,city=city,address=address,zip=zip,amount=amount,payment_method=radio)
                # myorder.save()
                return HttpResponse(f'this service is temprary off please try another payment method<br> <h3><a href="/checkbuy">try another way!</a></h3>')
            elif radio == 'cod':
                myorder = order(user=buyer,product=pro,first_name=first_name,last_name=last_name,email=email,phone=phone,
                state=state,city=city,address=address,zip=zip,amount=amount,payment_method=radio,payment_Status="cash on delivery")
                myorder.save()
                u = order.objects.filter(id=myorder.id).first()
                y = u.product
                if y[0:1]=='*':
                    allcart = cartItems.objects.filter(cart=request.user.id)
                    allcart.delete()
                return render(request,'cod.html',{'u':myorder})
            else:
                messages.error(request,'Somthing wronge try again!!')
                return redirect('/checkbuy')
        else:
            messages.warning(request,'Please confirm your address')
            return redirect('/checkbuy')
    return HttpResponse('error 404 page not found')


@csrf_exempt
def handlepayment(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            is_checksum = form[i]
        
    verify = checksum.verify_checksum(response_dict, MARCHANT_KEY, is_checksum)
    if verify:
        u = order.objects.filter(id=response_dict['ORDERID']).first()
        y = u.product
        if response_dict['RESPCODE'] == '01':
            u.payment_Status = f'Payment ({u.amount}) Done by PayTm'
            u.save()
            if y[0:1]=='*':
                allcart = cartItems.objects.filter(cart=u.user.id)
                allcart.delete()
        else:
            u.payment_Status = f'Payment ({u.amount}) Failed by PayTm'
            u.save()
        return render(request,"paymentstatus.html",{'response':response_dict,'u':u})
        