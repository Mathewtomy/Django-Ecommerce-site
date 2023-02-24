from django.db import models
import datetime
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
from django.contrib.sessions.models import Session

class Category(models.Model):
    category_name= models.CharField(max_length=50)
    def _str_(self):
        return self.category_name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
class Product_Category(models.Model):
    
   
    product_status=models.CharField(max_length=40)
   
    date = models.DateField (default=datetime.datetime.today)
    def _str_(self):
        return self.product_status    
    
class Product_option(models.Model):
    option=models.CharField(max_length=400)

class Product_option_name(models.Model):
    option_name=models.CharField(max_length=400)
    option_id= models.ForeignKey(Product_option,on_delete=models.CASCADE,default=1)
    
# Create your models here.
class Product(models.Model):
    name= models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image= models.CharField(max_length=2500)
    description= models.CharField(max_length=250, default='', blank=True,null=True)
    slug = models.SlugField(default="", null=False)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    status=models.ForeignKey(Product_Category,on_delete=models.CASCADE,default=1)
    # product_option=models.ForeignKey(Product_option,on_delete=models.CASCADE,default=1)
    # product_option_name=models.ForeignKey(Product_option_name,on_delete=models.CASCADE,default=1)
    
    def _str_(self):
        return self.name 
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter (id__in=ids)
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter (category=category_id)
        else:
            return Product.get_all_products();
        
class Product_option_description(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    
    product_option=models.ForeignKey(Product_option,on_delete=models.CASCADE,default=1)
    product_option_name=models.ForeignKey(Product_option_name,on_delete=models.CASCADE,default=1)
    
class Contact(models.Model):
    name= models.CharField(max_length=2500)
    email= models.CharField(max_length=255)
    address = models.CharField(max_length=2500)
    phone = models.IntegerField()
    
    
class About(models.Model):
    name= models.CharField(max_length=2500)
    # about_us= models.CharField(max_length=2500)

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField (max_length=50)
    phone = models.CharField(max_length=10)
    email=models.EmailField()
    password = models.CharField(max_length=100)
    def _str_(self):
        return self.first_name 
    #to save the data
    def register(self):
        self.save()


    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email= email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False
    
class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField (max_length=50, default='', blank=True)
    phone = models.CharField (max_length=50, default='', blank=True)
    date = models.DateField (default=datetime.datetime.today)
    status = models.BooleanField (default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-id')

class Return(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order,
                                 on_delete=models.CASCADE)
  
    date = models.DateField (default=datetime.datetime.today)
    status = models.BooleanField (default=False)
    reason = models.CharField (max_length=250)
    
    def placeOrder(self):
        self.save()

    @staticmethod
    def get_return_by_customer(customer_id):
        return Return.objects.filter(customer=customer_id).order_by('-date')
    
# class Cart(models.Model):
#     product = models.ForeignKey(Product,
#                                 on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer,
#                                  on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     price=models.IntegerField()
#     date = models.DateField (default=datetime.datetime.today)
    
#     def subtotal(self):
#         return self.product.price * self.quantity


class CartItem(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    def total(self):
        return self.quantity * self.product.price
    
    def name(self):
        return self.product.name
    
    def price(self):
        return self.product.price
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()
    
    def augment_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save()       


class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date = models.DateField (default=datetime.datetime.today)
    def __str__(self):
        return self.name
    

class Banner(models.Model):
    name=models.CharField(max_length=40)
    image=models.CharField(max_length=2500)
    date = models.DateField (default=datetime.datetime.today)
   
class Blog(models.Model):
    name=models.CharField(max_length=40)
    blog=models.CharField(max_length=500)
    image=models.CharField(max_length=2500)
    date = models.DateField (default=datetime.datetime.today)
    def __str__(self):
        return self.name  
    




   
    

    