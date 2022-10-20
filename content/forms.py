from socket import fromshare
from django import forms

paymentChoices = {
    ('Bank', 'Direct Bank Transfer'),
    ('Cash', 'Cash on delivery'),
    ('Paypal', 'Paypal'),
    ('Stripe', 'Stripe')
}

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    company_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    street = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    apartment = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    town = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    zip = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    shipping_address = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'custom-control-input', 'id':'checkout-diff-address'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Notes about your order, e.g. special notes for delivery', 'class': 'form-control'}))
    payment = forms.ChoiceField(required=False, choices=paymentChoices, widget=forms.RadioSelect(), )
    payment_description= forms.CharField(max_length=2000)


