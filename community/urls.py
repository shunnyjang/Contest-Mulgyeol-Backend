from django.urls import path
from .APIs import community, charity

urlpatterns = [
    path('', community.CommunityView.as_view(), name='community'),
    path('<int:pk>/', community.CommunityDetailView.as_view(), name='community'),
    path('charity/', charity.CharityView.as_view(), name='charity'),
    path('charity/<int:pk>/', charity.CharityDetailView.as_view(), name='charity-detail'),
]
