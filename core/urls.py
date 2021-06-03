from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from core import views


app_name = 'core'

urlpatterns = [
    # Url paths for django rest framework simple jwt
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('create/', views.CreateUserApiView.as_view(), name="create"),
    path('account/', views.ManageUserApiView.as_view(), name="account"),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name="token_verify"),
]
