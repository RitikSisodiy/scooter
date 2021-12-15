from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.base import Model
from ckeditor.fields import RichTextField
import json
import random ,string
from django.utils.text import slugify
def get_random_string(size):
    return ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = size))

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    slug=slugify(new_slug)
    Klass = instance
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = slugify(str(slug)+get_random_string(4))
        return unique_slug_generator(instance, new_slug=new_slug)
    return slugify(slug)
# Create your models here.
class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    state = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    zip = models.CharField(max_length=10)
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
    description = RichTextField(max_length=500)
    image = models.ImageField(upload_to="img",default ="")
    slug = models.SlugField(blank=True)

    def __str__(self):
        return str(self.name +" ("+ self.color +")")
    def save(self, *args, **kwargs):
        if len(self.slug)<1:
            self.slug = unique_slug_generator(Product,self.name)
        super(Product, self).save(*args, **kwargs)



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
    ('On-The-Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('pending','pending'),
)

class OrderPlaced(models.Model):
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.FloatField(blank=True,max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICE,default='pending')

    def save(self, *args, **kwargs):
        if self.order_id is None and self.order_date and self.id:
            self.order_id = self.order_date.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
class orderaddress(models.Model):
    order = models.OneToOneField(OrderPlaced,on_delete=models.CASCADE,related_name="address") 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

class TestDrive(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    bikemodel = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    question = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)


class Contact(models.Model):
    email = models.EmailField(max_length=50)
    name = models.CharField(max_length=30)
    phone = models.IntegerField()
    sub = models.CharField(max_length=500)
    question = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now=True)

class test(models.Model):
    testfield = models.CharField(max_length=50000)
    def jsondata(self):
        # Call remote service to get latitude & longitude
        latitude = json.loads(self.testfield)
        return latitude
    def save(self, *args, **kwargs):
        self.testfield = json.dumps(self.testfield)
        return super().save(*args, **kwargs)
class contactinfo(models.Model):
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    address = models.TextField()