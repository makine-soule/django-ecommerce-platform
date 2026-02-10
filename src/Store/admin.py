from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "brand",
        "price"
    ]

    search_fields = ("title",)

@admin.register(models.Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]

    search_fields = ("name",)
