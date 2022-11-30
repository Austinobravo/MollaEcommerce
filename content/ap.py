import js2py
import json  
# from .models import *
# code_2 = "function f(x) {return x+x;}"
# res_2 = js2py.eval_js(code_2)
  
# print(res_2(5))

# clear="function clearFtn() {'cart was cleared' }"
# clear_cart=js2py.eval_js(clear)
# print(clear_cart())


def clear(request):
    cart = json.loads(request.COOKIES['cart'])
    cart={}
    print('Cart:', cart)
    print('cookies:', request.COOKIES)
    order={
        'get_cart_total':0,
        'get_cartitems_total':0,
        'shipping': False

    }
    cartitems= order['get_cartitems_total']

    for i in cart:
        try:
            cartitems = cartitems+ cart[i]["quantity"]
            order['get_cart_total']
            order['get_cartitems_total']+=cart[i]["quantity"]
        except:
            pass