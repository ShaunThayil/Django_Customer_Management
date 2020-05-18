from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user,allowed_users,admin_only
from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from .filter import OrderFilter

@unauthenticated_user  # If user is already logged in; Don't Let Him Access Login Page
def loginPage(request):
    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if(user is not None):
            login(request,user)
            return redirect('home')   # Login Successful
        else:
            messages.info(request,"Username Or Password is Incorrect")   # Login Failed
    context = {}
    return render(request,'Accounts/login.html',context)   

@unauthenticated_user
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if(request.method == 'POST'):
        form = CreateUserForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            username = form.cleaned_data.get('username')
            # Execution Passes On To The post_save signal
            messages.success(request,"Account Was Created For " + username)
            return redirect('login')
    context = {'form':form}
    return render(request,'Accounts/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')  # Prevent Acces From Unlogged Users
@admin_only   # Only For Home: Allow Admins Only Else Redirect To User Page
def home(request):
    #return HttpResponse("<h1>Hello!!</h1>")

    orders = Order.objects.all().order_by('-date_created')
    customers = Customer.objects.all()
    total_orders = orders.count()
    delivered_count = orders.filter(status = 'Delivered').count()
    pending_count = orders.filter(status = 'Pending').count()
    context = {'orders':orders,'customers':customers,'total_orders': total_orders,'delivered_count':delivered_count,'pending_count':pending_count}
    return  render(request,'Accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    customer = request.user.customer
    #print(orders)
    total_orders = orders.count()
    delivered_count = orders.filter(status='Delivered').count()
    pending_count = orders.filter(status='Pending').count()
    context = {'customer':customer,'orders':orders,'total_orders':total_orders,'delivered_count':delivered_count,'pending_count':pending_count}
    return render(request,'Accounts/user.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    product = Product.objects.all()
    return  render(request,"Accounts/products.html",{"products":product})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
   
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return  render(request,"Accounts/customer.html",context)

@login_required(login_url='login')
@allowed_users(['customer'])
def account_setting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid:
            form.save()
    context = {'form':form}
    return render(request,'Accounts/account_settings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    if(pk == "new"):
        form = OrderForm()
    else:
        customer = Customer.objects.get(id=pk)
        form = OrderForm(initial={'customer':customer})
    
    if(request.method == 'POST'):
        # print("Request : ",request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    return render(request,'Accounts/order_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if(request.method == 'POST'):
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    context = {"form":form}
    return render(request,"Accounts/order_form.html",context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'Accounts/delete.html', context)


