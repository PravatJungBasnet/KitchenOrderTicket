from django.contrib import admin
from .models import Tables, Menu, Order, Category


@admin.register(Tables)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "is_occupied")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["table"]


# Register your models here.
