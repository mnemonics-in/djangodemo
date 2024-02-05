from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def allcategories(request):
    c=Category.objects.all()
    return render(request,template_name='category.html',context={'c':c})
def products(request,p):
    c=Category.objects.get(name=p)
    p=Product.objects.filter(category=c)
    return  render(request,template_name='products.html',context={'c':c,'p':p})
def productdetails(request,p):
    d = Product.objects.get(name=p)
    return render(request,template_name='productdetails.html',context={'d':d})

def signup(request):
    if(request.method=="POST"):
        username=request.POST['un']
        password=request.POST['pw']
        cpassword=request.POST['cp']
        fname=request.POST['fn']
        lname=request.POST['ln']
        emailid=request.POST['ei']


        if(password==cpassword):
            user=User.objects.create_user(username=username,password=password,first_name=fname,
                                                last_name=lname,email=emailid)
            user.save()
            return redirect('shop:allcategories')
        else:
            return HttpResponse("Passwords are not same")
    return render(request,template_name='signup.html')

def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcategories')
        else:
            return HttpResponse("Invalid Credentials")
    return render(request,template_name='login.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect('shop:login')