from django.contrib import admin
from .models import OrderMenu,Order


admin.site.register(Order)
admin.site.register(OrderMenu)