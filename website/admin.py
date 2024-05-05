from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import User, Category, Wish, WishReservation

class WishReservationsInline(admin.TabularInline):
    model = WishReservation

class WishInline(admin.TabularInline):
    model = Wish

class WishCategoryInline(admin.TabularInline):
    model = Wish.categories.through

@admin.register(User)
class UserAdmin(ModelAdmin):
    inlines = (WishReservationsInline, WishInline)

@admin.register(Category)
class CategoriesAdmin(ModelAdmin):
    inlines = (WishCategoryInline, )

@admin.register(Wish)
class WishAdmin(ModelAdmin):
    pass