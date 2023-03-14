from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']

class QueryForm(forms.ModelForm):
    class Meta:
        model = OrderQuery
        fields = ['email', 'issue']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image', 'search_tag1', 'search_tag2', 'search_tag3']

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckoutAddress
        fields = ['country', 'zip', 'street_address', 'nearest_landmark', 'email']
