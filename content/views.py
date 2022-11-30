from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .forms import *
from .utils import *
from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.contrib.auth.models  import User
from django.contrib.auth import authenticate, login, logout
import json
import stripe
import datetime
from django.contrib import messages
from .decorators import *
from django.views.generic import View
from django.views.generic.base import TemplateView

# Create your views here.

#Home View
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

#Cart
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

#Separate product id
def CartId(request, pk):
    product=Product.objects.get(id=pk)
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
        'cartitems': cartitems,
        'product':product
    }
    return render(request, 'product.html',context)

#Checkout
class Checkout(View):
    def get(self,request, *args, **kwargs):
        form= CheckoutForm()

        if self.request.user.is_anonymous:
            CookieData = CookieCart(self.request)
            cartitems=CookieData['cartitems']
            order=CookieData['order']
            items=CookieData['items']
        else:
            customer= self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer,order_complete=False)
            items=order.orderitem_set.all()
            cartitems= order.get_cartitems_total

        context={
            'items':items,
            'order':order,
            'cartitems': cartitems,
            'form': form
            

        }
        return render(self.request, 'checkout.html', context)
    def post(self,request, *args, **kwargs):

        transaction_id= datetime.datetime.now().timestamp()
        form = CheckoutForm(self.request.POST or None)
        try:
            if form.is_valid():
                city = form.cleaned_data.get('city')
                country = form.cleaned_data.get('country')
                house = form.cleaned_data.get('house')
                suite = form.cleaned_data.get('suite')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')
                description = form.cleaned_data.get('description')
                payment = form.cleaned_data.get('payment')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                phone = form.cleaned_data.get('phone')
                email = form.cleaned_data.get('email')
                
                if self.request.user.is_authenticated:
                    customer= self.request.user.customer
                    order, created = Order.objects.get_or_create(customer=customer,order_complete=False)
                else:
                                        
                    try:
                        customer = Customer.objects.create(email=email)
                        customer.first_name=first_name 
                        customer.last_name=last_name
                        customer.phone=phone
                        customer.save()
                        order, created=Order.objects.get_or_create(customer=customer, order_complete=False)

                        items=order.orderitem_set.all()
                        for item in items:
                            product=Product.objects.get(id=item['product']['id'])
                            orderitem=OrderItem.objects.create(product=product, order=order,quantity=item['quantity'])
                            orderitem.save()
                            
                    except:
                        return redirect('v')
            
                shipping_address= ShippingAddress(
                    customer=customer,
                    order=order,
                    house=house,
                    suite=suite,
                    country=country,
                    description=description,
                    city=city,
                    zip=zip,
                    state=state,
                )
                shipping_address.save()
                
                # order.shipping_address=shipping_address
                # order.save()
                if payment =='stripe':
                    return redirect('/payment/stripe')
                elif payment =='paypal':
                    return redirect('/payment/paypal')
                elif payment =='bank':
                    return redirect('/payment/bank')
                elif payment =='cash':
                    return redirect('/payment/bank')
                else:
                    messages.info(request, 'Invalid payment option')
                    return redirect('checkout')
            else:
                messages.info(request, 'You have no order')
                return redirect('home')

        except:
            return redirect('/') 

# Stripe Gateway Integration
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePayment(View):
    def get(self, request, *args, **kwargs):
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

        return render(request, 'stripe.html', context)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            try:
                order = Order.objects.get(customer=customer, order_complete=False)
            except:
                messages.info(request, 'You have no order')
                return redirect('home')
            #address= ShippingAddress.objects.get(customer=customer, order=order)

        else:
            customer=Customer.objects.all().last()
            try:
                order = Order.objects.get(customer=customer, order_complete=False)
            except:
                messages.info(request, 'You have no order')
                return redirect('home')
        price=int(order.get_cart_total)*100
        quantity=order.get_cartitems_total
        # try:
        if request.POST.get('submit') =="stripe":
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                        'name': 'Your cart',
                        },
                        'unit_amount': price,
                    },
                    'quantity': quantity,

                    },
                ],
                mode='payment',
                success_url=settings.BASE_URL + '/success/',
                cancel_url=settings.BASE_URL + '/cancel/',
                )
            #Create the Payment
            payment = Stripe_Payment()
            payment.stripe_charge_id = checkout_session['id']
            payment.user = self.request.user
            payment.price=float(order.get_cart_total)
            payment.save()

            #Giving the Order a Payment
            order.stripe_payment=payment
            order.save()

            return redirect(checkout_session.url) 
        
#Success View
class SuccessView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = self.request.user.customer
            try:
                order = Order.objects.get(customer=customer, order_complete=False) 
            except:
                messages.info(request, 'You do not have an order')
                return redirect('home')
            try:   
                address= ShippingAddress.objects.get(customer=customer, order=order)
            except:
                messages.info(request, 'You do not have a shipping address.')
                return redirect('checkout')
            items=order.orderitem_set.all()
            total=order.get_cart_total
            #cartitems= order.get_cartitems_total
            person=order.customer
            house=address.house
            transcation=order.transaction_id
        else:
            customer=Customer.objects.all().last()
            try:
                order = Order.objects.get(customer=customer, order_complete=False) 
            except:
                messages.info(request, 'You do not have an order')
                return redirect('home')
            try:   
                address= ShippingAddress.objects.get(customer=customer, order=order)
            except:
                messages.info(request, 'You do not have a shipping address.')
                return redirect('checkout')
            CookieData = CookieCart(request)
            person=order.customer
            house=address.house
            transcation=order.transaction_id
            #cartitems=CookieData['cartitems']
            total=CookieData['order']['get_cart_total']
            items=CookieData['items']

        context={
            'person': person,
            'address': address,
            'house':house,
            'items':items,
            'order':total,
            'transaction_id':transcation
            #'cartitems': cartitems

        }
        
        #Completing the order
        order.order_complete=True
        order.save()
        messages.success(request, 'Your order was successful')

        return render(request, 'success.html', context)


class CancelView(TemplateView):
    template_name = "cancel.html"


#Registration
@authenticated_user
def registration(request):
    if request.method=='POST':
        if request.POST.get('submit') == 'register':
            username= request.POST.get('register-username')
            first_name= request.POST.get('register-first-name')
            last_name= request.POST.get('register-last-name')
            email= request.POST.get('register-email')
            phone= request.POST.get('register-phone')
            password= request.POST.get('register-password')
            password2= request.POST.get('register-password-2')

            try:
                #Checking if the credentials -- Usename, Email -- exists
                if password==password2:
                    if User.objects.filter(username=username).exists():
                        messages.info(request, 'Username Already exists..')
                        return redirect('registration')
                    elif len(username)<5:
                        messages.info(request, 'Username must be up to 5 characters')
                        return redirect('registration')
                    elif User.objects.filter(email=email).exists():
                        messages.info(request, 'Email Already exists..')
                        return redirect('registration')

                    
                    else:
                        #if phone number exists
                        if Customer.objects.filter(phone=phone).exists():
                            messages.info(request, 'Phone number Already exists')  
                            return redirect('registration')  

                        #Creating a new User
                        newuser = User.objects.create_user(username=username,password=password, email=email)
                        newuser.first_name= first_name
                        newuser.last_name=last_name
                        newuser.password2=password2
                        newuser.save()
                else:
                    messages.info(request, "Password doesn't match..")
            except:
                return redirect('/')
            #Making the new user a customer
            try:
                if User:
                        customer = Customer.objects.create(user=newuser, email=email)
                        customer.first_name=first_name 
                        customer.last_name=last_name
                        customer.phone=phone
                        customer.save()
                        messages.info(request, 'Successfully created user. Please Login')
                        return redirect('registration')

                else:
                    messages.info(request, 'Please register...')
                    return redirect('registration')

            except:
                return redirect('v')
                #Creating the login page
        elif request.POST.get('submit') == 'login':
            login_name= request.POST.get('singin-login')
            login_email= request.POST.get('singin-login')
            login_password=request.POST.get('singin-password')

            user= authenticate(username=login_name, email=login_email, password=login_password)

            if user is not None:
                login(request, user)
                messages.info(request, 'Login Successfully...')
                return redirect('home')
                
            else:
                messages.info(request, 'Invalid Credentials')
           
    if request.user.is_anonymous:
            CookieData = CookieCart(request)
            cartitems=CookieData['cartitems']
            order=CookieData['order']
            items=CookieData['items']
    else:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,order_complete=False)
        items=order.orderitem_set.all()
        cartitems= order.get_cartitems_total

    context={
            'items':items,
            'order':order,
            'cartitems': cartitems,
        }    
    return render(request, 'registration.html', context)   

#Signout page
@unauthenticated_user
def signout_page(request):
        if request.user.is_anonymous:
            CookieData = CookieCart(request)
            cartitems=CookieData['cartitems']
            order=CookieData['order']
            items=CookieData['items']
        else:
            customer= request.user.customer
            order, created = Order.objects.get_or_create(customer=customer,order_complete=False)
            items=order.orderitem_set.all()
            cartitems= order.get_cartitems_total

        context={
            'items':items,
            'order':order,
            'cartitems': cartitems,
        }

        return render(request, 'logout.html', context)

#Logout function
def signout(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('registration') 

#Newsletter Email
def newsletter(request):
    if request.method=="POST":
        email=request.POST.get('newsletter')

        if Newsletter.objects.filter(email=email).exists():
            messages.error(request, 'Already subscribed...')
            return redirect('newsletter')
        else:
            newsform=Newsletter()
            newsform.email=email
            newsform.save()

            
        return render(request, 'newsletter.html', {'email':email})
    else:
        if request.user.is_anonymous:
            CookieData = CookieCart(request)
            cartitems=CookieData['cartitems']
            order=CookieData['order']
            items=CookieData['items']
        else:
            customer= request.user.customer
            order, created = Order.objects.get_or_create(customer=customer,order_complete=False)
            items=order.orderitem_set.all()
            cartitems= order.get_cartitems_total
        
        context={
                'items':items,
                'order':order,
                'cartitems': cartitems,

            }
        return render(request, 'newsletter.html', context)

#Search bar
def search(request):
    if request.method =='POST':
        mobile_search = request.POST.get('search_button')
        search_result= Product.objects.filter(name__contains=mobile_search)
        search_transaction_id_result=Order.objects.filter(transaction_id__contains=mobile_search)

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
            'cartitems': cartitems,
            'items': items,
            'order': order,
            'mobile_search': mobile_search,
            'search_result': search_result,
            'search_transaction_id_result':search_transaction_id_result,
            

            }

        return render(request, 'search.html', context
        )
    else:
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
            'cartitems': cartitems,
            'items': items,
            'order': order
            }

        return render(request, 'search.html', context)

#Order id
def get_transaction(request, pk):
    order = Order.objects.get(id=pk, order_complete=True)   
    address= ShippingAddress.objects.get(order=order)
    # payment= Physical_Payment.objects.get(physical_charge_id=order.transaction_id)
    items=order.orderitem_set.all()
    transcation=order.transaction_id
    total=order.get_cart_total
    cartitems= order.get_cartitems_total
    person=order.customer
    house=address.house
    
    
    context={
            'person': person,
            'address': address,
            'house':house,
            'items':items,
            'total':total,
            'order':order,
            'transaction_id':transcation,
            'cartitems': cartitems

        }        
    return render(request, 'order.html', context)

#Physical payment   
class PhysicalPayment(View):
    def get(self,request, *args, **kwargs):
        if self.request.user.is_authenticated:
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
        'cartitems': cartitems,

    }

        return render(self.request, 'bank.html', context)

    def post(self,request, *args, **kwargs):
        form=Physical_Payment()
        transaction_id= datetime.datetime.now().timestamp()
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            try:
                order = Order.objects.get(customer=customer, order_complete=False)
            except:
                messages.info(request, 'You have no order')
                return redirect('home')
            #address= ShippingAddress.objects.get(customer=customer, order=order)

        else:
            customer=Customer.objects.all().last()
            try:
                order = Order.objects.get(customer=customer, order_complete=False)
            except:
                messages.info(request, 'You have no order')
                return redirect('home')
            address, created= ShippingAddress.objects.get_or_create(customer=customer, order=order)

        if self.request.POST.get('submit')=='image':
            image=self.request.POST.get('image')
            #Giving the image a payment
            form.physical_charge_id=transaction_id
            form.customer=customer
            form.price=order.get_cart_total
            form.image=image
            form.save()
            #Giving the payment an order
            order.physical_payment=form
            order.transaction_id=transaction_id
            #Saving the Order
            
            order.save()
            return redirect('success')

#Paypal payment
class PaypalPayment(View):
    def get(self,request, *args, **kwargs):
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
        return render(self.request, 'paypal.html', context)

    def post(self,request, *args, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            try:
                order = Order.objects.get(customer=customer, order_complete=False)
            except:
                messages.info(request, 'You have no order')
                return redirect('home')
            
        else:
            customer=Customer.objects.all().last()
            try:
                order = Order.objects.get(customer=customer, order_complete=False)
            except:
                messages.info(request, 'You have no order')
                return redirect('home')
        
        data = json.loads(request.body)
        print('Data:',data)
        transaction_id= datetime.datetime.now().timestamp()
        total = float(data['total'])
        order.transaction_id=transaction_id

        if total == order.get_cart_total:
             #Create the Payment
            payment = Paypal_Payment()
            payment.paypal_charge_id = transaction_id
            payment.user = self.request.user
            payment.price=float(order.get_cart_total)
            payment.save()

            #Giving the Order a Payment
            order.paypal_payment=payment
           
            #messages.success(request, 'Your Order was successful')
            return redirect('success')

        return JsonResponse('Payment was processed.', safe=False)
        
 
def payment(request):

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

    return render(request, 'payment.html', context)

#Updating buttons
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
   
    context={
    "cartTotal": order.get_cart_total,
}
    return JsonResponse(context, safe=False)
