from django.contrib import admin
from .models import CustomUser, Category, Response, Advertisement



admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Response)
admin.site.register(Advertisement)
