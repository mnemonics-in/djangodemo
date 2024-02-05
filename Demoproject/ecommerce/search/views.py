from django.shortcuts import render,redirect
from shop.models import Product
from django.db.models import Q
# Create your views here.
def search(request):
    query=""
    b=None
    if(request.method=="POST"):
        query=request.POST['q']
        if(query):
            productresult=Product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))
    return render(request,template_name='search.html',context={'query':query,'p':productresult})
