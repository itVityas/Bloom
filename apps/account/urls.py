from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.account.views.role import RoleListCreateView, RoleDetailedView
from apps.account.views.user_roles import (
    UserRolesListView, UserRolesDetailedView)
from apps.account.views.user import (
    UserListView, UserDetailedView, UserRetrieveView)
from apps.account.views.register import RegistrationView
from apps.account.views.change_password import ChangePasswordView
from apps.account.serializers.autorization import CustomTokenObtainPairSerializer


urlpatterns = [
    # jwt
    path('login/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer)),
    path('change_password/', ChangePasswordView.as_view()),
    path('register/', RegistrationView.as_view()),
    path('users/', UserListView.as_view()),
    path('user/<int:pk>/', UserDetailedView.as_view()),
    path('user/detailed/<int:pk>/', UserRetrieveView.as_view()),
    # user role
    path('role/', RoleListCreateView.as_view()),
    path('role/<int:pk>/', RoleDetailedView.as_view()),
    path('userroles/', UserRolesListView.as_view()),
    path('userroles/<int:pk>/', UserRolesDetailedView.as_view()),
]
