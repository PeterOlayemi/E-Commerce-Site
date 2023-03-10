from django.db import models
from django.contrib.auth.models import User

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

class Order(models.Model):
    sent_receipt = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    queried = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField()
    address = models.CharField(max_length=299)
    nearest_landmark = models.CharField(max_length=299)
    phone_number = models.CharField(max_length=11)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.product} by {self.buyer}, sent_receipt: {self.sent_receipt}, paid:{self.paid}, delivered:{self.delivered}, queried:{self.queried}'
    
class OrderQuery(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    issue = models.TextField(max_length=299)

    def __str__(self):
        return f'{self.buyer} on {self.order.product}'

class OrderReceipt(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    receipt = models.FileField(upload_to='images/')

    def __str__(self):
        return f'{self.order.buyer}'

class Review(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()

    def __str__(self):
        return f'{self.product} by {self.buyer}'
