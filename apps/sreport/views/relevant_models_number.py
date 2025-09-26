from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.permissions import IsAuthenticated

from apps.sreport.serializers.relevant_models_number import RelevantModelNumberSerializer
from apps.shtrih.models import Models
from apps.shtrih.serializers.model import ModelsSerializer
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Report'])
@extend_schema_view(
    post=extend_schema(
        summary='return models with filters',
        description=''' Если is_other_production_models == True то Where Model.production_code != 400
                        Если is_other_production_models == False то Where Model.production_code == 400
                        and relevance=True''',
        request=RelevantModelNumberSerializer,
        responses={
            200: OpenApiResponse(response=ModelsSerializer, description='Success'),
            400: OpenApiResponse(description='Bad request'),
            500: OpenApiResponse(description='Server error'),
        }
    )
)
class RelevantModelNumberView(APIView):
    serializer_class = RelevantModelNumberSerializer
    paginator_class = StandartResultPaginator
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RelevantModelNumberSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['is_other_production_models']:
                queryset = Models.objects.filter(relevance=True).exclude(production_code=400)
            else:
                queryset = Models.objects.filter(relevance=True, production_code=400)

            paginator = StandartResultPaginator()
            page = paginator.paginate_queryset(queryset, request, view=self)
            res_serializer = ModelsSerializer(page, many=True)
            return paginator.get_paginated_response(res_serializer.data)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
