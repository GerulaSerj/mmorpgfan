from django.urls import path
from .views import registration_view
from .views import CustomLoginView, CustomLogoutView, AdvertisementListView, subscriptions

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('advertisement/<int:pk>/respond/', views.respond_to_advertisement, name='respond_to_advertisement'),
    path('', AdvertisementListView.as_view(), name='home'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]