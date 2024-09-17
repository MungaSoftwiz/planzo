from django.contrib import admin
from django.urls import path
from .views import editProfile, profileView

app_name = 'profiles'

urlpatterns = [
    path('editprofile/', editProfile, name='editprofile'),
    path('profile/', profileView, name='profile'),
    path('', profileView, name='profile')
]