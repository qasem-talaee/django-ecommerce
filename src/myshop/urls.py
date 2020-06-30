"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('product/<slug:name>/', product, name='product'),
    path('category/<slug:name>/', category, name='category'),
    path('category/<slug:name>/page/<int:page>/', category_page, name='category_page'),
    path('shop/', shop, name='shop'),
    path('shop/page/<int:page>/', shop_page, name='shop_page'),
    path('cart/', cart, name='cart'),
    path('profile/', Profile, name='Profile'),
    path('login/', login, name='login'),
    path('contact/', contact, name='contact'),
    path('checkout/', checkout, name='checkout'),
    path('login_step2/', login_step2, name='login_step2'),
    path('logout/', logout, name='logout'),
    path('place_order/', place_order, name='place_order'),
    path('serach/', search, name='search'),
    path('serach/page/<int:page>/', search_page, name='search_page'),

    ####### CART URLS
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('update_cart/<int:id>/', update_cart, name='update_cart'),
    path('remove_cart/<int:id>/', remove_cart, name='remove_cart'),

    ####### Captcha url
    path('captcha/', include('captcha.urls')),

    path('^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)