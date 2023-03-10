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

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = OrderReceipt
        fields = ['receipt']

class QueryForm(forms.ModelForm):
    class Meta:
        model = OrderQuery
        fields = ['issue']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image', 'search_tag1', 'search_tag2', 'search_tag3']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'address', 'nearest_landmark', 'phone_number']
