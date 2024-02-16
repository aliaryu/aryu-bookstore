from django.contrib import admin
from .models import Order, OrderBook


admin.site.register([Order, OrderBook])