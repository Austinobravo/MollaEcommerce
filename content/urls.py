from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('payment/', views.payment, name="payment"),
    path('update_item/', views.updateitems, name="update_item"),
    path('process_order/', views.ProcessOrder, name="process_order"),
]