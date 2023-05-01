from django.contrib import admin
from .models import CustomUser, Category, Response, Advertisement, CustomUserManager

class ProductAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'rating', 'title', 'dateCreation')
    list_filter = ('author', 'rating', 'postCategory', 'dateCreation')
    search_fields = ('author', 'rating', 'title', 'postCategory')

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Response)
admin.site.register(Advertisement)
admin.site.register(CustomUserManager)