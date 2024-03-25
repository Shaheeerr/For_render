from django.urls import path 
from .views import *



urlpatterns = [
    path('',RegisterUserView.as_view(),name='RegisterUserView'),
    path('api/user/login/', UserLoginView.as_view(), name='user_login'),
    path('api/user/verify/', VerifyUserView.as_view(), name='verify_user'),
    path('api/user/logout/', LogoutView.as_view(), name='user_logout'),  # New logout endpoint
    path('api/resend-otp/', Otp_resend.as_view(), name='resend_otp'),

]
