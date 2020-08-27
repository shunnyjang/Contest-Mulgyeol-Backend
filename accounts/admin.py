from django.contrib import admin
from .models import User, PhoneAuth, Shelter

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['userID', 'name', 'phone', 'role']

@admin.register(PhoneAuth)
class PhoneAuthAdmin(admin.ModelAdmin):
    pass

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    pass