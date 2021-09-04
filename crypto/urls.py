from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/',register,name="register"),
    path('',index,name="index"),
    path('login/',login,name="login"),
    url('^', include('django.contrib.auth.urls')),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('login/',login,name="login"),
    path('logoutme/',logoutuser,name="logoutme"),
    path('coin/',coinstore,name="coinstore"),
    path('profile/',profile,name="profile"),

]