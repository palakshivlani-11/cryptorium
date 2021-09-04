import environ
from .models import *
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import auth
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
import requests
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import json



# Create your views here.

def index(request):
    user = request.user
    price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,LTC,XLM,ADA,USDT,MIOTA,TRX&tsyms=INR")
    price = json.loads(price_request.content)
    parms = {
        'user':user,
        'price':price,
    }
    return render(request,"index.html",parms)


# def index(request): 
#     headtitle = "Life Styles | Home"
#     user = request.user
#     #checks for employee or customer by is_Staff
#     if user.is_staff == False:
#         #checks for logged in
#         if user.is_authenticated:
#             usertype = "Customer"
#         else:
#             #prints None if user is not logged in
#             usertype = None
#         parms = {
#         'title':headtitle,
#         'usertype':usertype,
#         }
#         return render(request,'index.html',parms)


    
   
def register(request):
    parms = {
        'title':'Register'
    }
    if request.method == 'POST':
        username = request.POST['username']
        mobno = request.POST.get('mobno')
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if MyUser.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect('register')
            elif MyUser.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user = MyUser.objects.create(username=username,email=email,mobno=mobno)
                user.set_password(password1)
                user.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('registration/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.info(request,'Check email and Verify your account')
                #after that return to index
                return redirect('index')
        else:
            messages.info(request,'Password not matched')
            return redirect('signup')
    return render(request,'registration/signup.html',parms)



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def logoutuser(request):
    logout(request)
    return redirect('index')




def login(request):
    title = "Login | Crypto"
    if request.method == 'POST':
        #login with username and password
        mobno = request.POST['mobno']
        password = request.POST['password']
        user = auth.authenticate(mobno=mobno,password=password)
        #checking for one more condition that is_staff is false or not to prevent employees to login as customer.
        if user is not None:
            if user.is_active == True and user.is_staff == False:
                auth.login(request,user)
                messages.info(request,'Logged In Successfuly')
                return redirect('index')
            else:
                messages.info(request,'Activate Your Account First')
                return redirect('login')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'registration/login.html',{'title':title})

@login_required
def profile(request):
    title = "Profile | Crypto"
    user = request.user
    if user is None:
        return redirect('login')
    else:
        parms = {
            'user':user,
            'title':title,
        }
        return render(request,'profile.html',parms)



@login_required
def coinstore(request):
    title = "Coin Notification"
    if request.method == 'POST':
        user = request.user
        coin = request.POST.get('coin')
        coinprice = request.POST['coinprice']
        obj = Notification.objects.filter(us=user,coin=coin).first()
        print(obj)
        if obj is None:
            obj = Notification.objects.create(us=user,coin=coin,coinprice=coinprice)
            messages.info(request,'Successfully stored info')
            return redirect('index')
        obj.coinprice = coinprice
        obj.save()
        return redirect('index')
    return render(request,'coin.html',{'title':title})
        