from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('home/', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('signout/', views.signout, name="signout"),
    path('logout/', signout_page, name="logout"),
    path('search/', search, name="search"),
    path('newsletter/', newsletter, name="newsletter"),
    path('registration/', views.registration, name="registration"),
    path('checkout/', Checkout.as_view(), name="checkout"),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    # path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    #path('create-checkout-session/', views.create_checkout_session, name="create-checkout-session"), # new
    #path('', HomePageView.as_view(), name='shome'),
    path('cart/<str:pk>', CartId, name='cartid'),
    # path('config/', views.stripe_config),  # new
    path('payment/bank', PhysicalPayment.as_view(), name="physicalpayment"),
    path('payment/stripe', StripePayment.as_view(), name="stripepayment"),
    path('payment/paypal', PaypalPayment.as_view(), name="paypalpayment"),
    #path('payment/bank', PaypalPayment.as_view(), name="paypalpayment"),
    # path('payment/', payment, name="payment"),
    path('update_item/', views.updateitems, name="update_item"),
    path('order/<str:pk>', get_transaction, name="order"),
    #path('process_order/', views.processorder, name="process_order"),
]