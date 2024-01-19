from django.contrib import admin
from .models import User, Address, Staff, Role

admin.site.register([User, Address, Staff, Role])