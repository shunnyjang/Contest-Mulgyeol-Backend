from django.contrib import admin
from .models import Recruitment, Tag, Volunteer, DailyRecruitmentStatus


@admin.register(Recruitment)
class RecruitmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    pass


@admin.register(DailyRecruitmentStatus)
class DailyRecruitmentStatusAdmin(admin.ModelAdmin):
    pass
