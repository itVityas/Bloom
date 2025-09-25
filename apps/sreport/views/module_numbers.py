from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from apps.sreport.serializers.module_numbers import ModuleNumbersSerializer
from apps.shtrih.serializers.module import ModulesSerializer
from apps.shtrih.models import Modules


@extend_schema(tags=['Report'])
@extend_schema_view(
    post=extend_schema(
        summary='**Get module numbers**',
        description='Get module numbers',
        responses={200: ModulesSerializer,
                   400: OpenApiResponse(description='Bad request')}
    )
)
class ModuleNumbersView(APIView):
    serializer_class = ModuleNumbersSerializer

    def post(self, request):
        serializer = ModuleNumbersSerializer(data=request.data)
        if serializer.is_valid():
            is_segregation_needed = serializer.validated_data['is_segregation_needed']
            is_other_production_module_needed = serializer.validated_data['is_other_production_module_needed']

            if not is_segregation_needed and not is_other_production_module_needed:
                queryset = Modules.objects.all()

            res_serializer = ModulesSerializer(queryset, many=True)
            return Response(
                res_serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
