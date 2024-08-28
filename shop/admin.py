from django.contrib import admin
from .models import Product,Contact,Order

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','category')
    list_filter = ('category',)
    search_fields = ('product_name','category')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'razorpay_orderid','razorpay_paymentid','status')

admin.site.register(Product,ProductAdmin)
admin.site.register(Contact)
admin.site.register(Order,OrderAdmin)