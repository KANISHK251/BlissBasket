from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=30)
    category = models.CharField(max_length=50, default = "")
    subcategory = models.CharField(max_length=50, default = "")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default = "")


class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=70, default="")

class Order(models.Model):
     name = models.CharField(max_length=100)
     email = models.CharField(max_length=100)
     address = models.CharField(max_length=100)
     address2 = models.CharField(max_length=100, blank=True)
     city = models.CharField(max_length=100)
     state = models.CharField(max_length=100)
     zip_code = models.CharField(max_length=10)
     phone = models.CharField(max_length=10)
     razorpay_orderid = models.CharField(max_length=100,unique=True)
     razorpay_paymentid = models.CharField(max_length=100,blank=True, null=True)
     status = models.CharField(max_length=10,default="pending")