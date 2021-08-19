from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.base import Model
import json

# Create your models here.

class Customer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	locality = models.CharField(max_length=200)
	zipcode = models.IntegerField()
	city = models.CharField(max_length=200)
	Address = models.CharField(max_length=200)
	def __str__(self):
		return str(self.id)

class Product(models.Model):
	name = models.CharField(max_length=200)
	company = models.CharField(max_length=50,default="",blank=True)
	original_price = models.FloatField(null=True,blank=True)
	price = models.FloatField()
	ActualPrice = models.FloatField()
	color = models.CharField(max_length=20,default='', blank=True)
	category = models.CharField(max_length=50,default='', blank=True)
	description = models.TextField(max_length=500)
	image = models.ImageField(upload_to="img",default ="")

	def __str__(self):
		return str(self.name +" ("+ self.color +")")


class specs(models.Model):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    listele = models.CharField(max_length=100000)
    def jsondata(self):
        # Call remote service to get latitude & longitude
        latitude = json.loads(self.listele)
        return latitude
    def save(self, *args, **kwargs):
        self.listele = json.dumps(self.listele)
        return super().save(*args, **kwargs)
    
class prodimg(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE , related_name='prodimg')
    img = models.ImageField(upload_to="img",default ="prodimg/")
	
    def __str__(self):
        return str(self.product.name)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.price


STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.FloatField(blank=True,max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICE,default='pending')

    def save(self, *args, **kwargs):
        if self.order_id is None and self.order_date and self.id:
            self.order_id = self.order_date.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


class TestDrive(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    bikemodel = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    question = models.CharField(max_length=100)


class Contact(models.Model):
    email = models.EmailField(max_length=50)
    name = models.CharField(max_length=30)
    phone = models.IntegerField()
    sub = models.CharField(max_length=500)
    question = models.CharField(max_length=500)

class test(models.Model):
    testfield = models.CharField(max_length=50000)
    def jsondata(self):
        # Call remote service to get latitude & longitude
        latitude = json.loads(self.testfield)
        return latitude
    def save(self, *args, **kwargs):
        self.testfield = json.dumps(self.testfield)
        return super().save(*args, **kwargs)