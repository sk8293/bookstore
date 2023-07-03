from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth import login,logout,authenticate
from .forms import *
 
# Create your views here.
def home(request):
    books=Book.objects.all()
    context={'books':books}
    if request.user.is_staff:
        return render(request,'bookstore/adminhome.html',context)
    else: 
        return render(request,'bookstore/home.html',context)
 
def logoutPage(request):
    logout(request)
    return redirect('/')
 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print("working")
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'bookstore/login.html',context)
 
def registerPage(request):
    form=createuserform()
    cust_form=createcustomerform()
    if request.method=='POST':
        form=createuserform(request.POST)
        cust_form=createcustomerform(request.POST)
        if form.is_valid() and cust_form.is_valid():
            user=form.save()
            customer=cust_form.save(commit=False)
            customer.user=user 
            customer.save()
            return redirect('login')
    context={
        'form':form,
        'cust_form':cust_form,
    }
    return render(request,'bookstore/register.html',context)
 
def addbook(request):
    form=createbookform()
    if request.method=='POST':
        form=createbookform(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
 
    context={'form':form}
    return render(request,'bookstore/addbook.html',context)
 
def viewcart(request):
    cust=Customer.objects.filter(user=request.user)
    for c in cust:
        carts=Cart.objects.all()
        for cart in carts:
            if(cart.customer==c):
                context={
                    'cart':cart
                }
                return render(request,'bookstore/viewcart.html',context)  
        else:
            return render(request,'bookstore/emptycart.html') 
            
 
def addtocart(request,pk):
    book=Book.objects.get(id=pk)
    cust=Customer.objects.filter(user=request.user)
    
    for c in cust:       
        carts=Cart.objects.all()
        reqcart=''
        for cart in carts:
            if(cart.customer==c):
                reqcart=cart
                break
        if(reqcart==''):
            reqcart=Cart.objects.create(
                customer=c,
            )
        reqcart.books.add(book)    
    return redirect('/')


def checkout(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        order = Customer(user=request.user)
        order.save()
        for item in cart.books.all():
            order.add(item)
        cart.books.clear()
        
        # Redirect to the order confirmation page
        return redirect('/')
    
    # If the request method is GET, render the checkout page
    return render(request, 'bookstore/checkout.html')
