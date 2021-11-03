from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, GetUsersListApi, GetUserDetailApi
)

app_name = 'authentication'
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('get_users_list/', GetUsersListApi.as_view()),
    path('get_user_detail/', GetUserDetailApi.as_view()),
]
