from django.db import models
from store.models import *
from customers.models import *

# Create your models here.



STATUS = (
        ('OrderPending', 'Orderpending'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
         ('Returned', 'Returned'),
    )



class Orders(models.Model):
    PAYMENT_METHODS=(
       
        ('Razorpay','Razorpay'),
        ('COD','COD'),
    )
    
    user                = models.ForeignKey(Account,on_delete=models.CASCADE, null=False)
    delivery_address    = models.ForeignKey(Addresses,on_delete=models.CASCADE)
    order_number        = models.CharField(max_length=20)
    oder_total          = models.DecimalField(max_digits=10, decimal_places=2, null=False,default=0)
    payment_method      = models.CharField(max_length=30,choices=PAYMENT_METHODS,null=True,blank=True)
    grand_total         = models.DecimalField(max_digits=10, decimal_places=2, null=False,default=0)
    
    cart                = models.ForeignKey(Cart,on_delete=models.CASCADE)
    products            = models.ForeignKey(Products,on_delete=models.CASCADE)
    variant             = models.ForeignKey(Variants,on_delete=models.CASCADE)
    cartitem            = models.ForeignKey(CartItem,on_delete=models.CASCADE)
    quantity            = models.IntegerField()
    
    order_date          = models.DateTimeField(auto_now_add=True)
    status              = models.CharField(max_length=20,choices=STATUS, default='Orderpending', null=True,blank=False)
    is_active           = models.BooleanField(default=True,null=True)
    