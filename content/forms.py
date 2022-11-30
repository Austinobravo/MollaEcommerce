from django import forms
from .models import *


paymentChoices = {
    ('bank', 'Direct Bank Transfer'),
    ('cash', 'Cash on delivery'),
    ('paypal', 'Paypal'),
    ('stripe', 'Stripe')
}

class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=False,max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False,max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class':'form-control'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    house = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'House number and Street name'}))
    suite = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apartments, suite, unit etc ...'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    zip = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    #shipping_address = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'custom-control-input', 'id':'checkout-diff-address'}))
    description = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder':'Notes about your order, e.g. special notes for delivery', 'class': 'form-control'}))
    payment = forms.ChoiceField(required=False, choices=paymentChoices, widget=forms.RadioSelect(), )
    #payment_description= forms.CharField(max_length=2000)

class NewsletterForm(forms.Form):
    email=forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Enter your Email Address", 'aria-label':"Email Adress"}))
class PhysicalPaymentForm(forms.Form):
    class Meta:
        model=Physical_Payment
        fields =('image')
