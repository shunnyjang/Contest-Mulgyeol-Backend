from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view(), name='post'),
    path('apply/', views.VolunteerView.as_view(), name='volunteer')
]
