from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from app.users.views import UserRegisterView, SuperUserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('register-superuser/', SuperUserRegisterView.as_view(), name='user-register-superuser'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
