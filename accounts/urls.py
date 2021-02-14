from django.urls import path
from .APIs import signin, signup, shelter

urlpatterns = [
    path('', signin.LoginTestView.as_view()),
    path('signup/', signup.UserCreateView.as_view(), name='signup'),
    path('id/', signup.CheckIdView.as_view(), name="check_id"),
    path('auth/', signup.PhoneAuthView.as_view(), name="phone_auth"),
    path('login/', signin.LoginJWTView.as_view(), name="login"),
    path('shelter/', shelter.ShelterCreateView.as_view(), name="create_shelter"),
    path('shelter/<int:pk>/', shelter.ShelterDetailView.as_view(), name="detail_shelter"),
]
