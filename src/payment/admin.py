from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# Register your models here.

@admin.register(ShippingAddress)
class AdminShippingAddress(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "address1",
    )

@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "amount_paid",
        "date_ordered",
    ]


@admin.register(OrderItem)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "quantity",
        "product",
        "price",
    ]