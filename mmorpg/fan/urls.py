from django.urls import path
from .views import registration_view
from .views import CustomLoginView, CustomLogoutView, AdvertisementListView, subscriptions
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('register/', cache_page(60*10),  registration_view, name='register'),
    path('login/', cache_page(60*10), CustomLoginView.as_view(), name='login'),
    path('logout/', cache_page(60*10), CustomLogoutView.as_view(), name='logout'),
    path('advertisement/<int:pk>/respond/', cache_page(60*10), views.respond_to_advertisement, name='respond_to_advertisement'),
    path('', AdvertisementListView.as_view(), cache_page(60*10), name='home'),
    path('subscriptions/', cache_page(60*10), subscriptions, name='subscriptions'),
]