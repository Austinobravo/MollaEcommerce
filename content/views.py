from itertools import product
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import *
from .utils import *
import json
import datetime
# Create your views here.
def home(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,order_complete=False)
        items=order.orderitem_set.all()
        cartitems= order.get_cartitems_total
    else:
        CookieData = CookieCart(request)
        cartitems=CookieData['cartitems']
        order=CookieData['order']
        items=CookieData['items']
        
    context={
        'products': products,
        'cartitems': cartitems,
        'items': items,
        'order': order
         }

    return render(request, 'home.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,order_complete=False)
        items=order.orderitem_set.all()
        cartitems= order.get_cartitems_total

    else:
        CookieData = CookieCart(request)
        cartitems=CookieData['cartitems']
        order=CookieData['order']
        items=CookieData['items']
        
    context={
        'items':items,
        'order':order,
        'cartitems': cartitems

    }
    return render(request, 'cart.html', context)

def checkout(request):
    form = CheckoutForm()
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,order_complete=False)
        items=order.orderitem_set.all()
        cartitems= order.get_cartitems_total
        
    else:
        CookieData = CookieCart(request)
        cartitems=CookieData['cartitems']
        order=CookieData['order']
        items=CookieData['items']
        

    context={
        'items':items,
        'order':order,
        'form': form,
        'cartitems': cartitems

    }
   

    return render(request, 'checkout.html', context)
def payment(request):

    return render(request, 'payment.html')
def updateitems(request):
    data = json.loads(request.body)
    productId =data['productId']
    action =data['action']

    print('action:', action)
    print('productId:', productId)

    customer= request.user.customer
    product= Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,order_complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action=='add':
        orderitem.quantity=(orderitem.quantity + 1)
    elif action=='remove':
        orderitem.quantity=(orderitem.quantity - 1)
    orderitem.save()

    if orderitem.quantity <= 0 or action=='delete':     
        orderitem.delete()
   

    return JsonResponse('item was added', safe=False)

def ProcessOrder(request):
    transaction_id= datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,order_complete=False)
        
    else:
        print('cookies:', request.COOKIES)
        first_name =  data['form']['first_name']  
        last_name =  data['form']['last_name']  
        email =  data['form']['email']  
        phone =  data['form']['phone'] 

        CookieData = CookieCart(request)
        items=CookieData['items'] 

        customer, created = Customer.objects.get_or_create(email=email)
        customer.first_name=first_name 
        customer.last_name=last_name
        customer.phone=phone
        customer.save()

        order=Order.objects.create(customer=customer, order_complete=False)
        for item in items:
            product=Product.objects.get(id=item['product']['id'])
            orderitem=OrderItem.objects.create(product=product, order=order,quantity=item['quantity'])
    
    total = float(data['form']['total'])
    order.transaction_id=transaction_id

    if total == float(order.get_cart_total):
        order.order_complete=True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            house = data['shipping']['house'],
            suite = data['shipping']['suite'],
            state = data['shipping']['state'],
            city = data['shipping']['city'],
            zip = data['shipping']['zip'],
            country = data['shipping']['country'],
            description = data['shipping']['description'],
            #payment = data['shipping']['payment'],
        )        
            
    return JsonResponse('Payment was processed.', safe=False)

# Hey, might be a year late!
# Here is an easy fix for the card-total without reload!

# Add this line instead of "location.reload"

# document.getElementById('total-items').innerText = data['cartTotal']

# Then in your views.py for updateitem add this these lines:

# context={
#     "cartTotal": order.get_cart_total_quantity(),
# }
# return JsonResponse(context, safe=False)

# Then just make sure, in every place where there is a cart-total to be displayed, add the ID of "total-items"