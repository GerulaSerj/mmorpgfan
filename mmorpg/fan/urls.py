from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, AdvertisementListView, subscriptions, AdvertisementUpdate, AdvertisementDelete, registration_view
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('register/', cache_page(60*10)(registration_view), name='register'),
    path('login/', cache_page(60*10)(CustomLoginView.as_view()), name='login'),
    path('logout/', cache_page(60*10)(CustomLogoutView.as_view()), name='logout'),
    path('advertisement/<int:pk>/respond/', views.respond_to_advertisement, name='respond_to_advertisement'),
    path('', AdvertisementListView.as_view(), name='home'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('articles/<int:pk>/update/', AdvertisementUpdate.as_view(), name='advertisement_edit'),
    path('articles/<int:pk>/delete/', AdvertisementDelete.as_view(), name='advertisement_delete'),
]