from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import RegisterUserView, ResetPasswordView, ValidateUserView, ValidateNewPasswordView

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('registration/', RegisterUserView.as_view()),
    path('registration/validation/', ValidateUserView.as_view()),
    path('password-reset/', ResetPasswordView.as_view()),
    path('password-reset/validation/', ValidateNewPasswordView.as_view()),
]
