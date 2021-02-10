from django.urls import path
from . import views
from .APIs import applyment, recruitment

urlpatterns = [
    path('', recruitment.RecruitmentView.as_view(), name='recruitment_list'),
    path('<int:pk>/', recruitment.RecruitmentDetailView.as_view(), name='recruitment_detail'),
    path('status/', applyment.list_of_volunteer_for_shelter.as_view(), name='volunteer_status'),
    path('apply/', applyment.VolunteerApplyView.as_view(), name='volunteer_apply'),
    path('list/', applyment.list_of_applying_volunteer_of_user.as_view(), name='applying_volunteer_list'),
]
