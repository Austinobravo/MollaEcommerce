from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return f"{self.first_name} | {self.last_name}"

class Product(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    price = models.FloatField()
    order_product= models.BooleanField(default=False, null=True, blank=True)
    first_image = models.ImageField(null=True, blank=True)
    second_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    @property
    def ImageFIRSTURL(self):
        try:
            url=self.first_image.url
        except:
            url = ''
        return url
    @property
    def ImageSECONDURL(self):
        try:
            url=self.second_image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    order_complete=models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200,null=True,blank=True)

    def  __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = True
        orderitems = self.orderitem_set.all()
        for order in orderitems:
            if order.product.order_product == False:
                shipping=True
        return shipping



    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cartitems_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.customer.user} | {self.product}"
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    house = models.CharField(max_length=200,null=True,blank=True)
    suite = models.CharField(max_length=200,null=True,blank=True)
    country = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    zip = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=200,null=True,blank=True)
    #payment = models.Rad(required=False, widget=models.RadioSelect() )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.house} | {self.order}"

