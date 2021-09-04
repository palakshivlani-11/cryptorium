from django.contrib import admin
from .models import *
#from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm, MyUserChangeForm

 # Register your models here.

# admin.site.register(EnrollUser)




class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ['username','email','mobno']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobno',)}),
    ) #this will allow to change these fields in admin module


admin.site.register(MyUser, MyUserAdmin)



admin.site.register(Notification)
