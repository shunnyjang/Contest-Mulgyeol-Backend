from django.urls import path
from . import views

urlpatterns = [
    path('', views.CommunityView.as_view(), name='community'),
]
