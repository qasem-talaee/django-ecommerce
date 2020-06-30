from django.db import models
from .models_app import get_submenu_choice
from django.utils.timezone import *
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=500)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    postal_code = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Users detail'
        verbose_name = 'Users detail'

    def __str__(self):
        return '%s' % (self.name)

class Sender_way(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image/sender_way/%Y/%m/%d')
    description = models.TextField()
    status = models.BooleanField()
    price_per_weight = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        verbose_name = 'Sender ways'
        verbose_name_plural = 'Sender ways'

    def __str__(self):
        return '%s' % (self.name)


class Category(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='image/category/%Y/%m/%d')
    submenu_id = models.CharField(choices=get_submenu_choice(), max_length=5, default='0')

    class Meta:
        verbose_name_plural = 'Category'
        verbose_name = 'Category'

    def __str__(self):
        return '%s' % (self.name)

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image/product/%Y/%m/%d')
    desc = RichTextUploadingField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sender = models.ForeignKey(Sender_way, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

    def __str__(self):
        return '%s' % (self.name)

class Reduction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    percent = models.DecimalField(max_digits=2, decimal_places=0)
    expired_time = models.DateField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Reductions'
        verbose_name = 'Reductions'

    def __str__(self):
        return '%s' % (self.expired_time)

class Contact(models.Model):
    CONTACT_STATUS = (
        ('0', 'Do not answered'),
        ('1', 'Answered'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=500)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=5, choices=CONTACT_STATUS)
    id_ip = models.CharField(max_length=20, default=0)

    class Meta:
        verbose_name = 'Contacts'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return '%s is contact for %s' % (self.name, self.subject)

class Coupon(models.Model):
    coupon_id = models.CharField(max_length=50)
    is_infinite = models.BooleanField(default=False)
    count = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    status = models.BooleanField(default=True)
    expired_time = models.DateField(auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Coupons'
        verbose_name = 'Coupons'

    def __str__(self):
        if self.count == '':
            return '%s coupon is %s' % (self.coupon_id, self.count)
        else:
            return '%s coupon is infinite' % (self.coupon_id)

class Cart_non_user(models.Model):
    ip_address = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.DecimalField(max_digits=10, decimal_places=0)
    date = models.DateField(auto_now_add=True)
    coupon_id = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Deserted carts'
        verbose_name = 'Deserted carts'

    def __str__(self):
        return '%s' % (self.ip_address)

class Cart_user(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.DecimalField(max_digits=10, decimal_places=0)
    payed = models.BooleanField(default=False)
    send_status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    coupon_id = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Carts'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return '%s' % (self.user_id)
