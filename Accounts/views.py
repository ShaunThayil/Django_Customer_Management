from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import OrderForm,CreateUserForm
from .filter import OrderFilter


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if(user is not None):
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Username Or Password is Incorrect")
    context = {}
    return render(request,'Accounts/login.html',context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if(request.method == 'POST'):
        form = CreateUserForm(request.POST)
        if(form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,"Account Was Created For " + username)
            return redirect('login')
    context = {'form':form}
    return render(request,'Accounts/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')  # Prevent Acces From Unlogged Users
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
def products(request):
    product = Product.objects.all()
    return  render(request,"Accounts/products.html",{"products":product})

@login_required(login_url='login')
def customer(request,pk):
   
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return  render(request,"Accounts/customer.html",context)

@login_required(login_url='login')
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
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'Accounts/delete.html', context)


