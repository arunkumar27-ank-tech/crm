from django.forms import  inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from django.contrib import messages
from django.forms.models import ModelForm
from accounte.models import Product
from django.shortcuts import redirect, render

from django.http import HttpResponse
from .models import *
from.filters import *
from .decorators import admin_only, allowed_users, unauthenticated_user
from .forms import OrderForm, RegisterForm, SettingsForms
from .signals import customer_profile

@unauthenticated_user
def register(request):
    
    form = RegisterForm()
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() 
            username = form.cleaned_data.get('username')                       
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request,'accounte/register.html', context)

@unauthenticated_user
def loginpage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or password is incorrect ')

    context={}
    return render(request, 'accounte/login.html', context)

@login_required(login_url='login')
def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customer = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    orders_delivered = orders.filter(status='order delivered').count()
    orders_pending = orders.filter(status='pending').count()

    context = {'customer':customer,'orders':orders,'total_orders':total_orders,'orders_delivered':orders_delivered,
    'orders_pending':orders_pending}
    return render(request,'accounte\dashboard.html',context)

def accountsettings(request):
    customer = request.user.customer
    form = SettingsForms(instance=customer)
    if request.method == 'POST':
        form = SettingsForms(request.POST, request.FILES, instance=customer)
        if form.is_valid():
          
            form.save()
    context = {'form':form}
    return render(request, 'accounte/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    product = Product.objects.all()
    context = {'product':product}
    return render(request,'accounte\product.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'orders':orders,'customer':customer,'myFilter':myFilter}
    return render(request,'accounte\customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    orders_delivered = orders.filter(status='order delivered').count()
    orders_pending = orders.filter(status='pending').count()


    context = {'orders':orders,'total_orders':total_orders,
    'orders_delivered':orders_delivered,'orders_pending':orders_pending}
    return render(request,'accounte/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order, fields=('product','status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method=='POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request,'accounte/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method=='POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounte/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request,'accounte/delete_order.html', context)