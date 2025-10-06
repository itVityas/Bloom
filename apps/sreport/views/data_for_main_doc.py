import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.permissions import IsAuthenticated

from Bloom.paginator import StandartResultPaginator
from apps.sreport.serializers.data_for_main_doc import DataForMainDocSerializer
from apps.shtrih.models import Protocols
from apps.shtrih.serializers.protocols import ProtocolsFullSerializer


@extend_schema(tags=['Report'])
@extend_schema_view(
    post=extend_schema(
        summary='return data for main doc',
        description='''return data for main doc''',
        responses={
            200: OpenApiResponse(response=DataForMainDocSerializer, description='Success'),
            400: OpenApiResponse(description='Bad request'),
            500: OpenApiResponse(description='Server error'),
        }
    )
)
class DataForMainDocView(APIView):
    serializer_class = DataForMainDocSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandartResultPaginator

    def post(self, request):
        receive_serializer = DataForMainDocSerializer(data=request.data)
        if receive_serializer.is_valid():
            queryset = Protocols.objects.all()
            if receive_serializer.validated_data['is_period']:
                if receive_serializer.validated_data['from_date']:
                    queryset = queryset.filter(work_date__gte=receive_serializer.validated_data['from_date'])
                if receive_serializer.validated_data['to_date']:
                    queryset = queryset.filter(work_date__lte=receive_serializer.validated_data['to_date'])
            if receive_serializer.validated_data['is_month']:
                month = time.strftime('%m')
                queryset = queryset.filter(work_date__month=month)
            if receive_serializer.validated_data['model']:
                queryset = queryset.filter(product__model__name__short_name=receive_serializer.validated_data['model'])
            if receive_serializer.validated_data['module']:
                queryset = queryset.filter(workplace__module__number=receive_serializer.validated_data['module'])
            if receive_serializer.validated_data['shift']:
                queryset = queryset.filter(shift=receive_serializer.validated_data['shift'])
            if receive_serializer.validated_data['is_other_production']:
                queryset = queryset.exclude(product__model__production_code=400)
            else:
                queryset = queryset.filter(product__model__production_code=400)

            paginator = StandartResultPaginator()
            page = paginator.paginate_queryset(queryset, request, view=self)
            res_serializer = ProtocolsFullSerializer(page, many=True)
            return paginator.get_paginated_response(res_serializer.data)

        return Response(receive_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
