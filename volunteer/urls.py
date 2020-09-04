from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view(), name='post'),
    path('post/', views.PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('status/', views.VolunteerRetrieveView.as_view(), name='volunteer_status'),
    path('apply/', views.VolunteerApplyView.as_view(), name='volunteer_apply'),
    path('list/', views.UserVolunteerRetrieveView.as_view(), name='volunteer_list'),
]
