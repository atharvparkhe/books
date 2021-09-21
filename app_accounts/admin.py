from django.contrib import admin
from .models import *


class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "points", "is_verified"]


admin.site.register(CustomerModel, CustomerModelAdmin)
