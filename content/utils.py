from .models import *
import json

def CookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart={}
    print('Cart:', cart)
    items=[]
    order={
        'get_cart_total':0,
        'get_cartitems_total':0,
        'shipping': False

    }
    cartitems= order['get_cartitems_total']

    for i in cart:
        try:
            cartitems = cartitems+ cart[i]["quantity"]

            product= Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            order['get_cart_total']+=total
            order['get_cartitems_total']+=cart[i]["quantity"]

            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'ImageFIRSTURL':product.ImageFIRSTURL,
                    'ImageSECONDURL':product.ImageSECONDURL,
                    },
                'quantity':cart[i]["quantity"],
                'get_total': total
                }
            items.append(item)

            if product.order_product == False:
                order['shipping'] =True
        except:
            pass

    return{'cartitems': cartitems, 'order': order, 'items': items}