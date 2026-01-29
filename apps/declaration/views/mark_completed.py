from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.declaration.models import Declaration


@extend_schema(tags=['Declarations'])
@extend_schema_view(
    get=extend_schema(
        summary='Mark declaration completed',
        description='Permission: admin, declaration_reader',
        responses={
            200: {'description': 'Mark completed'},
            404: {'description': 'Not found'},
        }
    ),
)
class MarkCompletedView(APIView):
    def get(self, request):
        try:
            declaration = Declaration.objects.exclude(declared_items__available_quantity__gt=0).distinct()
            declaration.update(is_completed=True)
            return Response({'count': declaration.count()})
        except Exception as ex:
            return Response(
                {'error': str(ex)},
                status=status.HTTP_404_NOT_FOUND
            )
