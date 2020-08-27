from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('id/', views.CheckIdView.as_view(), name="check_id"),
    path('auth/', views.PhoneAuthView.as_view(), name="phone_auth"),
    path('login/', views.LoginJWTView.as_view(), name="login"),
    path('shelter/', views.ShelterCreateView.as_view(), name="create_shelter"),
    path('shelter/<int:pk>/', views.ShelterDetailView.as_view(), name="detail_shelter"),
]
