from django.contrib import admin

# Register your models here.

from sklint.models import *

admin.site.register([Client, Category, Product, Cart, CartProduct, Order])
