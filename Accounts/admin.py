from django.contrib import admin

# Register your models here.
from .models import Customer,Product,Order,Tag


# Register The Models To See Them in Admin Panel
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)