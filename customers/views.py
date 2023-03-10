from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login, authenticate,logout,update_session_auth_hash
from .models import Account,Addresses
from store.models import *
from orders.models import *

from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control,never_cache
from django.utils.decorators import method_decorator

import smtplib 
import secrets
import re

# Create your views here.


def check_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff == False and request.user.is_superuser == False and request.user.is_active == True and request.user.is_blocked == False:
            return view_func(request, *args, **kwargs)
        else:
            messages.info(request,'Your account an admin')
            return redirect('user_login')
    return wrapper_func



@cache_control(no_cache = True,must_revalidate = False,no_store=True)
def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
       return redirect('home')
  
    main_banner = Banners.objects.get(id=1).banners
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    
    main_banner = Banners.objects.get(id=1).banners
    return render(request,'index.html',{'main_banner':main_banner,'sports':sports,'brands':brands ,'Products':Products})

@cache_control(no_cache = True,must_revalidate = False,no_store=True)
def register_view(request):
    if 'user' in request.session :
        return redirect('home')
    # if request.user.is_authenticated:
    #    return redirect('home')
   
    
          
    if request.method =='POST':
        email =request.POST['email']
        username =request.POST['username']
        passwrod1 =request.POST['password1']
        password2 =request.POST['password2']
        
        
        if email and username and passwrod1 and password2:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                # email is invalid
                error_message = "Please enter a valid email address."
                return render(request, 'signup.html', {'error_message': error_message})
    
            
            elif passwrod1 == password2:
                if Account.objects.filter(username=username).exists():
                    messages.info(request,'Username Taken')
                    return redirect('register')
                elif Account.objects.filter(email=email).exists():
                    messages.info(request,'Email Taken')
                    return redirect('register')
                else:
                    message = generate_otp()
                    sender_email  = "maxoutstores@gmail.com"
                    receiver_mail = email
                    password      = "aojgilhtcyfcyptj"
                   
                    server        = smtplib.SMTP("smtp.gmail.com",587)
                    server.ehlo()
                    server.starttls()
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_mail, message)
                    server.quit
                    
                    
                    user = Account.objects.create_user(username=username,password=passwrod1,email=email)
                    
                    user.save()
                    request.session['email'] = email
                    request.session['otp'] = message
                    hello = request.session['email']
                    print(hello)
                   
                    return redirect('verify_signup',)
                    #login(request, user)
                    # print('user created')
                    # return redirect('home')
            else:
                messages.info(request,'Password not matching')
                return redirect('register')
        else:
            messages.info(request,'Input every details')
            return redirect('register')
       
    else:
        return render(request,'signup.html') 
    
def generate_otp(length=6):
    #generate OTP with specific length
    return ''.join(secrets.choice("0123456789") for i in range(length))     
   
@cache_control(no_cache = True,must_revalidate = False,no_store=True)  
def verify_signup(request):
    
    if request.method == "POST":
     
        user = Account.objects.get(email=request.session['email'])
        x  = request.session.get('otp')
        print(user)
        OTP = request.POST['otp']
        
        if OTP == x:
            user.is_verified = True
            user.save()
            cart = Cart.objects.create(customer=user)
            del request.session['email'] 
            del request.session['otp']
            
            auth.login(request,user)
            return redirect('home')
        else:
            user.delete()
            messages.info(request,"invalid otp")
            return redirect('register')
    return render(request,'signup_verify.html') 
    
@never_cache
def user_login(request):
    if 'user' in request.session :
        return redirect('home')
    # if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_blocked:
    #    return redirect('home')
  
    
    if request.method== 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
       
        if email and password:
            user=authenticate(email=email,password=password)
            if user is not None and not user.is_blocked :
                if  user.is_verified:
                    print(user)
                    request.session['user_type'] = 'user'
                    login(request,user)
                    return redirect('home')
                else:
                    messages.info(request,'Your account is not verified')
                return redirect('user_login')
            else:
                messages.info(request,'Your account has been blocked')
                return redirect('user_login')
        else:
            messages.info(request,'Enter every details')
            return redirect('user_login')
    else:
         return render(request,'signin.html')
    
def logout(request):
    
    auth.logout(request)
    # del request.session['email']
    return redirect(index)

   
@login_required(login_url='user_login') 
@check_user
def home(request):
    
    context = {
        'main_banner':  Banners.objects.get(id=1).banners,
        'cart_count':   CartItem.objects.filter(cart= Cart.objects.get(customer = request.user)).count(),
        'sports':       Sport.objects.all(),
        'brands':       Brand.objects.all() ,
        'Products':     Products}
    return render(request,'home.html',context)
    # else:
    #     return redirect('user_login')

@login_required(login_url='user_login') 
@check_user
def profile(request):
    context = {
        'main_banner':  Banners.objects.get(id=1).banners,
        'cart_count':   CartItem.objects.filter(cart= Cart.objects.get(customer = request.user)).count(),
        'sports':       Sport.objects.all(),
        'brands':       Brand.objects.all() ,
        'user':         request.user,
        'Products':     Products,
        }
   
    return render(request,'user_profile.html',context)
    # else:
    #     return redirect('user_login')




@login_required(login_url='user_login') 
def update_username(request):
    context = {
    'main_banner':  Banners.objects.get(id=1).banners,
    'cart_count':   CartItem.objects.filter(cart= Cart.objects.get(customer = request.user)).count(),
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    'Products':     Products,
    }
   
    if request.method == 'POST':
        # Get the new username from the form data
        current_username = request.user.username
        new_username     = request.POST.get('new_username')
    
        # Update the user's username 
        if new_username and current_username: 
            user = request.user
            print(user)
           
            if Account.objects.filter(username=new_username).exists():
                messages.info(request,'Username already exists')
                return redirect('update_username') 
            else:
                user.username = new_username
                user.save()
                update_session_auth_hash(request, user)
        return redirect('profile')
    
    # If the request is not a POST request, render the change username template
    return render(request, 'update_user.html',context)

def upload_profile_img(request):
    context = {
    'main_banner':  Banners.objects.get(id=1).banners,
    'cart_count':   CartItem.objects.filter(cart= Cart.objects.get(customer = request.user)).count(),
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    'Products':     Products,
    }
   
    user           = request.user
    if  request.method == 'POST':
        
        profile_image         = request.FILES.get('image')
        user.profile_image = profile_image
        user.save()
        return redirect('profile')
    return render(request, 'upload_profile.html',context)
    
@login_required(login_url='user_login') 
def update_password(request):
    context = {
        'main_banner':  Banners.objects.get(id=1).banners,
        'cart_count':   CartItem.objects.filter(cart= Cart.objects.get(customer = request.user)).count(),
        'sports':       Sport.objects.all(),
        'brands':       Brand.objects.all() ,
        'user':         request.user,
        'Products':     Products,
        }
   
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password     = request.POST.get('new_password')
        user=request.user
         
        if current_password == new_password: 
            messages.info(request,'This is your previous password. Enter a new one.')
            return redirect('update_password')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    return render(request, 'update_password.html',context)

def address(request):
    context = {
        'main_banner':  Banners.objects.get(id=1).banners,
        'cart_count':   CartItem.objects.filter(cart= Cart.objects.get(customer = request.user)).count(),
        'sports':       Sport.objects.all(),
        'brands':       Brand.objects.all() ,
        'user':         request.user,
        'Products':     Products,
        'addresses':    Addresses.objects.filter(user_id=request.user),
        }

    return render(request, 'user_address.html', context)

def add_address(request):
    context = {
    'main_banner':  Banners.objects.get(id=1).banners,
    'cart_count':   CartItem.objects.filter(cart= Cart.objects.get(customer = request.user)).count(),
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    'Products':     Products,
    }


    user = request.user
    user_id = user.id
    print(user_id)
    
    if request.method == 'POST':
        first_name     = request.POST['first_name']
        last_name      = request.POST['last_name']
        house_name     = request.POST['house_name']
        street_name    = request.POST['street_name']
        city           = request.POST['city']
        district       = request.POST['district']
        state          = request.POST['state']
        pincode        = request.POST['pincode']
        mobile         = request.POST['mobile']
        
        if first_name and last_name and house_name and street_name and city and district and state and pincode and mobile :
            if not re.match(r'^\d{10}$', mobile):
                # email is invalid
                error_message = "Please enter a valid Mobile number."
                return render(request, 'add_address.html', {'error_message': error_message})
            
            else:
                if Addresses.objects.filter(user_id=user_id):
                    address = Addresses.objects.create(
                        first_name   = first_name,
                        last_name    = last_name,
                        house_name   = house_name,
                        street_name  = street_name,
                        city         = city,
                        district     = district,
                        state        = state,
                        pincode      = pincode,
                        mobile       = mobile,
                        user_id      = Account.objects.get(id=user_id)
                    )
                else:
                    address = Addresses.objects.create(
                        first_name   = first_name,
                        last_name    = last_name,
                        house_name   = house_name,
                        street_name  = street_name,
                        city         = city,
                        district     = district,
                        state        = state,
                        pincode      = pincode,
                        mobile       = mobile,
                        user_id      = Account.objects.get(id=user_id),
                        is_primary   = True,
                    )
            return redirect('address')
        else:
            messages.info(request,'Input all fields')
            return redirect('add_address')
    else:
        return render(request, 'add_address.html',context)
    
def delete_address(request,id):
    address = Addresses.objects.get(id=id)
    address.delete()
    return redirect('address')
    
def my_orders(request):
    context = {
        'main_banner':  Banners.objects.get(id=1).banners,
        'cart_count':   CartItem.objects.filter(cart= Cart.objects.get(customer = request.user)).count(),
        'sports':       Sport.objects.all(),
        'brands':       Brand.objects.all() ,
        'user':         request.user,
        'Products':     Products,
        'orders':      Orders.objects.filter(user = request.user).order_by('-id'),
        }
   
    return render(request,'my_orders.html',context)