from rest_framework.generics import (
    ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.account.models import User
from apps.account.serializers.user import UserSerializer, UserUpdateSerializer
from apps.account.permissions import AccountPermissions
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['jwt'])
@extend_schema_view(
    get=extend_schema(
        summary='Получение списка всех пользователй',
        description='isUser',
    ),
)
class UserListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = StandartResultPaginator


@extend_schema(tags=['jwt'])
@extend_schema_view(
    put=extend_schema(
        summary='Обновление пользователя',
        description='isAdmin',
    ),
    patch=extend_schema(
        summary='Частичное обновление пользователя',
        description='isAdmin',
    ),
    delete=extend_schema(
        summary='Удаление пользователя',
        description='isAdmin',
    ),
)
class UserDetailedView(DestroyAPIView, UpdateAPIView):
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


@extend_schema(tags=['jwt'])
@extend_schema_view(
    get=extend_schema(
        summary='Получение пользователя по id',
        description='isUser',
    )
)
class UserRetrieveView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
