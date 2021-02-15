from django.urls import path
from .APIs import applyment, recruitment

urlpatterns = [
    path('', recruitment.RecruitmentView.as_view(), name='recruitment_list'),
    path('<int:pk>/', recruitment.RecruitmentDetailView.as_view(), name='recruitment_detail'),
    path('daily/', recruitment.update_new_daily_recruitment_by_shelter, name='daily_recruitment_list'),
    path('daily/<int:pk>/', recruitment.DailyRecruitmentDetailView.as_view(), name='daily_recruitment_detail'),
    path('status/', applyment.list_of_volunteer_for_shelter, name='volunteer_status'),
    path('apply/', applyment.VolunteerApplyView.as_view(), name='volunteer_apply'),
    path('list/', applyment.list_of_applying_volunteer_of_user, name='applying_volunteer_list'),
]
