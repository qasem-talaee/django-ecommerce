from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
import datetime
from .models_app import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    def image_admin(self, obj):
        return mark_safe('<img src="{image}" class="img-fluid" width="90" />'.format(image=obj.image.url))
    def submenu(self, obj):
        if obj.submenu_id == 0:
            return mark_safe('Main category')
        else:
            return mark_safe('Sub Category')
    image_admin.short_description = 'Image'
    list_display = ('image_admin', 'name', 'submenu')
    search_fields = ('name',)

class SenderWayAdmin(admin.ModelAdmin):
    def image_admin(self, obj):
        return mark_safe('<img src="{image}" class="img-fluid" width="90" />'.format(image=obj.image.url))
    image_admin.short_description = 'Image'
    list_display = ('image_admin', 'name', 'status', 'price_per_weight', 'price')
    search_fields = ('name',)
    list_filter = ('status',)

class ProductAdmin(admin.ModelAdmin):
    def image_admin(self, obj):
        return mark_safe('<img src="{image}" class="img-fluid" width="20%" />'.format(image=obj.image.url))
    image_admin.short_description = 'Image'
    def name_admin(self, obj):
        return mark_safe('<a href="/product/{name}/" target="_blank">{name}</a>'.format(name=obj.name))
    name_admin.short_description = 'Name'
    list_display = ('image_admin', 'name_admin', 'price', 'weight', 'count', 'status', 'sender', 'category')
    list_filter = ('status', 'sender', 'category')
    search_fields = ('name',)

class ReductionAdmin(admin.ModelAdmin):
    def now(self, obj):
        return mark_safe(datetime.datetime.now().strftime('%m %d, %Y'))
    def product_admin(self, obj):
        offer = Reduction.objects.get(id=obj.id)
        product = Product.objects.filter(id=offer)
        for i in product:
            return mark_safe('<img src="{image}" class="img-fluid" width="20%" />').format(image=i.image.url)
    now.short_description = 'Now date'
    product_admin.short_description = 'image'
    list_display = ('product', 'percent', 'now', 'expired_time', 'status')
    list_filter = ('status',)

class ContactAdmin(admin.ModelAdmin):
    def id_admin(self, obj):
        user_count = User.objects.filter(id=obj.id_ip).count()
        if user_count == 0:
            return mark_safe('ip address : {ip}').format(ip=obj.id_ip)
        else:
            user = User.objects.filter(id=obj.id_ip)
            for i in user:
                name = i.name
                return mark_safe('User name : {name}').format(name=name)
    id_admin.short_description = 'User or Ip'
    list_display = ('name', 'email', 'subject', 'date', 'status', 'id_admin')
    list_filter = ('status',)
    search_fields = ('name', 'email', 'subject')

class CartnonuserAdmin(admin.ModelAdmin):
    def product_admin(self, obj):
        cart = Cart_non_user.objects.filter(id=obj.id)
        for i in cart:
            product = Product.objects.filter(id=i.product_id)
            for j in product:
                return mark_safe('<a href="/product/{name}/" target="_blank">{name}</a>'.format(name=j.name))
    def product_image(self, obj):
        cart = Cart_non_user.objects.filter(id=obj.id)
        for i in cart:
            product = Product.objects.filter(id=i.product_id)
            for j in product:
                return mark_safe('<img src="{image}" class="img-fluid" width="20%" />'.format(image=j.image.url))
    product_admin.short_description = 'Product'
    product_image.short_description = 'Image'
    list_display = ('ip_address', 'product_admin', 'product_image', 'count', 'date', 'coupon_id')

class CartuserAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        cart = Cart_user.objects.filter(id=obj.id)
        for i in cart:
            product = Product.objects.filter(id=i.product_id)
            for j in product:
                return mark_safe('<a href="/product/{name}/" target="_blank">{name}</a>'.format(name=j.name))
    def product_image(self, obj):
        cart = Cart_user.objects.filter(id=obj.id)
        for i in cart:
            product = Product.objects.filter(id=i.product_id)
            for j in product:
                return mark_safe('<img src="{image}" class="img-fluid" width="20%" />'.format(image=j.image.url))
    def user_name(self, obj):
        cart = Cart_user.objects.filter(id=obj.id)
        for i in cart:
            user = User.objects.filter(name=i.user_id)
            for j in user:
                return mark_safe('{name}'.format(name=j.name))
    product_image.short_description = 'image'
    product_name.short_description = 'Product name'
    user_name.short_description = 'user name'
    list_display = ('user_name', 'product_image', 'product_name', 'count', 'payed', 'send_status', 'date', 'coupon_id')
    list_filter = ('payed', 'send_status')

class CouponAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile',)
    search_fields = ('name', 'email', 'mobile', 'address', 'postal_code')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Sender_way, SenderWayAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Reduction, ReductionAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Cart_non_user, CartnonuserAdmin)
admin.site.register(Cart_user, CartuserAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(User, UserAdmin)