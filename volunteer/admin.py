from django.contrib import admin
from .models import Post, Tag, Volunteer, UserVolunteer

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    pass

@admin.register(UserVolunteer)
class UserVolunteerAdmin(admin.ModelAdmin):
    pass