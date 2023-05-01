from django.contrib import admin
from .models import CustomUser, Category, Response, Advertisement, Subscription

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author')
    filter_horizontal = ('subscriptions',)

admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Subscription)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Response)