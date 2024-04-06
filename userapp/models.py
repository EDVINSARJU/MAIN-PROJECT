from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings


class CustomUser(AbstractUser):
    ADMIN=1
    STAFF=2
    CUSTOMER=3
    

    USER_TYPES = (
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (CUSTOMER, 'Customer'),
        
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, default='3')
    username=models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
     
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    def _str_(self):
        return self.username
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
      
class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    addressline1 = models.CharField(max_length=50, blank=True, null=True)
    addressline2 = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True)

    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    age = property(calculate_age)

    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender)

    def str(self):
        return self.user.username
    
    def get_role(self): 
        if self.user_type == 2:
            user_role = 'Staff'
        elif self.user_type == 3:
            user_role = 'Customer'
        return user_role
    from django.db import models
    

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    purity_of_gold = models.CharField(max_length=10, default='18k')  
    quantity = models.IntegerField(default=1)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=(("active", "Active"), ("inactive", "Inactive")))
    product_image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    making_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gold_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stone_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gold_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_purity = models.FloatField(null=True, blank=True)
        
    def calculate_sale_price(self):
        if self.discount is not None:
            discounted_price = self.price - (self.price * (self.discount / 100))
        else:
            discounted_price = self.price

        sale_price = discounted_price + self.making_charge + (self.gold_value * self.gold_weight) + self.stone_cost
        gst_amount = sale_price * (self.gst_rate / 100)
        return round(sale_price + gst_amount, 2)
        
    def save(self, *args, **kwargs):
        # Convert self.discount and self.gold_weight to floats
        self.discount = float(self.discount) if self.discount is not None else None
        self.gold_weight = float(self.gold_weight)

        # Calculate sale price without saving it to the instance
        self.sale_price = self.calculate_sale_price()
        
        try:
            gold_item = self.gold_item
        except GoldItemNew.DoesNotExist:
            gold_item = None

        if gold_item and gold_item.volume > 0:
            known_density = 19.32  # Known density of pure gold (in g/cm^3)
            density = self.gold_weight / gold_item.volume
            self.estimated_purity = (density / known_density) * 100

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name
    
    
    
    
class GoldItemNew(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name='gold_item')
    weight = models.FloatField()
    volume = models.FloatField()
    calculated_purity = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.calculated_purity is None:
            # Calculate estimated purity if not provided
            known_density = 19.32  # Known density of pure gold (in g/cm^3)
            density = self.weight / self.volume
            self.calculated_purity = (density / known_density) * 100
        super().save(*args, **kwargs)
    
    
    
    
    
from django.db import models
from django.conf import settings
from .models import Product

class ShoppingCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def calculate_total_price(self):
        return self.quantity * self.product.sale_price
















from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


from django.db import models

class Feedback(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()



from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    pincode = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return self.username











class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    razorpay_payment_id = models.CharField(max_length=255)
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_signature = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=20)
    payment_date = models.DateTimeField(auto_now_add=True)