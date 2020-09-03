from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view(), name='post'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('status/', views.VolunteerRetrieveView.as_view(), name='volunteer-status'),
    path('apply/', views.VolunteerApplyView.as_view(), name='volunteer-apply'),
]
