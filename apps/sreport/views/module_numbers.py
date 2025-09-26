from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.permissions import IsAuthenticated

from apps.sreport.serializers.module_numbers import ModuleNumbersSerializer
from apps.shtrih.serializers.module import ModulesSerializer
from apps.shtrih.models import Modules
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Report'])
@extend_schema_view(
    post=extend_schema(
        summary='**Get module numbers**',
        description='''
        is_segregation_needed - без прочей продукции,
        is_other_production_module_needed - только прочая продукция''',
        responses={200: ModulesSerializer,
                   400: OpenApiResponse(description='Bad request')}
    )
)
class ModuleNumbersView(APIView):
    serializer_class = ModuleNumbersSerializer
    pagination_class = StandartResultPaginator
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ModuleNumbersSerializer(data=request.data)
        if serializer.is_valid():
            is_segregation_needed = serializer.validated_data['is_segregation_needed']
            is_other_production_module_needed = serializer.validated_data['is_other_production_module_needed']

            if not is_segregation_needed and not is_other_production_module_needed:
                queryset = Modules.objects.all()
            elif is_segregation_needed:
                queryset = Modules.objects.exclude(workplaces__type_of_work__id=6).distinct()
            else:
                queryset = Modules.objects.filter(workplaces__type_of_work__id=6).distinct()

            paginator = StandartResultPaginator()
            page = paginator.paginate_queryset(queryset, request, view=self)
            res_serializer = ModulesSerializer(page, many=True)
            return paginator.get_paginated_response(res_serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
