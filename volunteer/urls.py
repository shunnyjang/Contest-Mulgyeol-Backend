from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view(), name='post'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('apply/', views.VolunteerView.as_view(), name='volunteer')
]
