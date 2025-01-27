from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.account.serializers.change_password import ChangePasswordSerializer


@extend_schema(tags=['jwt'])
@extend_schema_view(
    patch=extend_schema(
        summary='Изменение пароля',
        description='isUser',
    ),
)
class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user
