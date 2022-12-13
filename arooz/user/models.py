from django.db import models
from versatileimagefield.fields import VersatileImageField
from tinymce.models import HTMLField
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser,
 )

# Create your models here.


class Login(AbstractUser):
    is_customer = models.BooleanField(default=False)
    

class Customer(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='user')
    customer_name = models.CharField(max_length = 100,null=True)
    phone_number = models.CharField(default=0, null=True, max_length=10, unique = True)  
    email = models.EmailField(max_length=254,null=True)
    address = models.CharField(max_length = 250)
  
    
class AdminNumber(models.Model):
    name = models.CharField(max_length=20)
    phone_number=models.CharField(max_length=12)    
    
class Category(models.Model):
    category = models.CharField(max_length = 200, unique=True)
    image = VersatileImageField(upload_to="categories/", null=True)
    
    
    
    def get_absolute_url(self):
        return reverse_lazy("user:shop", kwargs={"id": self.id})
    
    def get_subcategories(self):
        return SubCategory.objects.filter(category=self) 
    
    def get_product(self):
        return Product.objects.filter(category=self) 
    
    def __str__(self):
        return str(self.category)
         

    
    
class SubCategory(models.Model):
    subcategory = models.CharField(max_length = 150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy("user:product", kwargs={"id": self.id})

    def get_shop_url(self):
        return reverse_lazy("user:shop", kwargs={"id": self.id})
    
    def get_products(self):
        return Product.objects.filter(subcategory=self) 
    
    def __str__(self):
        return str(self.subcategory)
       

    
class Product(models.Model):
    # user=models.ForeignKey(Customer, on_delete=models.CASCADE, null=True,default='')
    product = models.CharField(max_length = 150)
    image = VersatileImageField(upload_to="products/", null=True)
    sub_image1 = VersatileImageField(upload_to="products/", null=True,blank=True)
    sub_image2 = VersatileImageField(upload_to="products/", null=True,blank=True)
    sub_image3 = VersatileImageField(upload_to="products/", null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    offer_price = models.IntegerField(null = True)
    rentalsecurity = models.CharField(max_length = 250,null=True,blank=True)
    quantity = models.IntegerField(default = 0)
    description = models.CharField(max_length = 250)
    is_top_save_today= models.BooleanField(default = False)
    is_best_seller = models.BooleanField(default = False)
        
    def __str__(self):
        return self.product
    

class MainBanner(models.Model):
    bannerbig = VersatileImageField(upload_to="MainBanner/", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,blank=True )
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True,blank=True )

    

class SubBanners1(models.Model):
    subbanner1 = VersatileImageField(upload_to="SubBanners/", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
    
class SubBanners2(models.Model):
    subbanner2 = VersatileImageField(upload_to="SubBanners/", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    


class HeaderFlash(models.Model):
    address =  models.CharField(max_length = 150)
    offer_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.address


 
    
    
    
class Cart(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True,default='')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product
    
     
class Wishlist(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True,default='')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,default='',null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
    # def get_products(self):
    #     return Product.objects.filter(product=self) 
    


class ChangePassword(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, blank=True, null=True)
    forgot_password_token = models.CharField(max_length=100)
    created_at = models. DateTimeField(auto_now_add = True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
 
    
def get_absolute_url(self):
    return reverse("_detail", kwargs={"pk": self.pk})



       
class Measurements(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True,default='')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True,default='')
    sleevelength = models.CharField(max_length = 150,null=True, default=0 )
    chestaround = models.CharField(max_length = 150,null=True, default=0 )
    waistAround = models.CharField(max_length = 150,null=True, default=0 )
    LengthTrouser = models.CharField(max_length = 150,null=True, default=0 )
    hip = models.CharField(max_length = 150,null=True, default=0 )
    WaistForTrouser = models.CharField(max_length = 150,null=True, default=0 )
    thighs = models.CharField(max_length = 150,null=True, default=0 )
    hem = models.CharField(max_length = 150,null=True, default=0 )

    def __str__(self):
        return self.user.customer_name
    
class Size(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True,default='')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True,default='')
    size = models.CharField(max_length = 150,null=True, default=0 )
    
    def __str__(self):
        return self.user.customer_name
    
class Event(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True,default='')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True,default='')
    date = models.DateField()
    
    def __str__(self):
        return self.user.customer_name

class AddToCart(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True,default='')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE,null=True,default='')
    added_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, default=1)
    total = models.IntegerField(null=True)
    
   
    def __str__(self):
        return self.product.product