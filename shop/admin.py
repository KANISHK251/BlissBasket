from django.contrib import admin
from .models import Product,Contact

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','category')
    list_filter = ('category',)
    search_fields = ('product_name','category')

admin.site.register(Product,ProductAdmin)
admin.site.register(Contact)