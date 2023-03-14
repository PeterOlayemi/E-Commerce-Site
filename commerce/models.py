from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import secrets
from .paystack import Paystack

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=99)
    
    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    name = models.CharField(max_length=99, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=299, blank=True, null=True)
    price = models.FloatField(default=0.00)
    image = models.ImageField(upload_to='images/')
    search_tag1 = models.CharField(max_length=19)
    search_tag2 = models.CharField(max_length=19, blank=True, null=True)
    search_tag3 = models.CharField(max_length=19, blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'
    
    def number_of_likes(self):
        return self.likes.count()

class Cart(models.Model):
    queried = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.product} by {self.buyer}, Ordered:{self.ordered}, Queried: {self.queried}'
    
    def get_price(self):
        return self.quantity * self.price

class CheckoutAddress(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    nearest_landmark = models.CharField(max_length=299)
    email = models.EmailField()

    def __str__(self):
        return self.buyer.username

class Payment(models.Model):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	price = models.PositiveIntegerField()
	ref = models.CharField(max_length=199)
	email = models.EmailField()
	verified = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-date_created',)

	def __str__(self):
		return f"Payment: {self.price}"

	def save(self, *args, **kwargs):
		while not self.ref:
			ref = secrets.token_urlsafe(50)
			object_with_similar_ref = Payment.objects.filter(ref=ref)
			if not object_with_similar_ref:
				self.ref = ref

		super().save(*args, **kwargs)
	
	def price_value(self):
		return int(self.price) * 100

	def verify_payment(self):
		paystack = Paystack()
		status, result = paystack.verify_payment(self.ref, self.price)
		if status:
			if result['amount'] / 100 == self.price:
				self.verified = True
			self.save()
		if self.verified:
			return True
		return False
    
class OrderQuery(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    email = models.EmailField()
    issue = models.TextField(max_length=299)

    def __str__(self):
        return f'{self.buyer} on {self.order.product}'

class Review(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()

    def __str__(self):
        return f'{self.product} by {self.buyer}'
