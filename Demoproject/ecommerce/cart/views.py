from django.shortcuts import render,HttpResponse
from shop.models import Product
from cart.models import Cart
from cart.models import Account,Order
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def cartremove(request,n):
    p=Product.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()
            p.stock += 1
            p.save()


        else:
            cart.delete()
            p.stock += 1
            p.save()

    except:
        pass
    return cartview(request)
@login_required
def fullremove(request,n):
    p=Product.objects.get(name=n)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass
    return cartview(request)
@login_required
def cartview(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total+=i.quantity*i.product.price

    return render(request,template_name='cartview.html',context={'c':cart,'total':total})
@login_required
def addtocart(request,n):
    p=Product.objects.get(name=n)
    u=request.user#current login
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock > 0):
            cart.quantity+=1
            cart.save()
            p.stock-=1
            p.save()

    except:
        if(p.stock > 0):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock-=1
            p.save()
    return cartview(request)
@login_required
def orderform(request):
    if(request.method=='POST'):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']

        u=request.user
        cart=Cart.objects.filter(user=u)
        total=0
        for i in cart:
            total +=i.quantity*i.product.price


        try:
            num=int(n)
            ac=Account.objects.get(acctnum=n)
            if(ac.amount>=total):
                ac.amount=ac.amount-total
                ac.save()
                for i in cart:
                    o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
                    o.save()
                cart.delete()
                msg="You Order Placed Successfully"
                return render(request,template_name='orderdetail.html',context={'msg':msg})
            else:
                msg="Insufficient Amount.You can't place Order"
                return render(request,template_name='orderdetail.html',context={'msg':msg})
        except:
            pass


    return render(request,template_name='orderform.html')
@login_required

def orderview(request):
    u = request.user
    o = Order.objects.filter(user=u)


    return render(request,template_name='orderview.html',context={'o':o,'u':u.username})