from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CheckoutAddress)
admin.site.register(OrderQuery)
admin.site.register(Review)
admin.site.register(Payment)
