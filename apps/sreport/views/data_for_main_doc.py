import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.permissions import IsAuthenticated

from Bloom.paginator import StandartResultPaginator
from apps.sreport.serializers.data_for_main_doc import (
    DataForMainDocSerializer,
    DataForMainDocResponseSerializer
)
from apps.shtrih.models import Protocols


@extend_schema(tags=['Report'])
@extend_schema_view(
    post=extend_schema(
        summary='return data for main doc',
        description='''
        return data for main doc
        ordering:
            model_name
            -model_name
            variant_code
            -variant_code
            module
            -module
            shift
            -shift
            designation
            -designation

        group:
            model_name
            variant_code
            module
            shift
        ''',
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

            group = receive_serializer.validated_data['group']

            res_list = []
            model_name = ''
            variant_code = ''
            module = 0
            shift = ''
            assembly = 0
            extract = 0
            packaging = 0
            for protocol in queryset.select_related():
                if group:
                    assembly = 0
                    extract = 0
                    packaging = 0
                    if group == 'model_name':
                        if protocol.product.model.name.short_name == model_name:
                            continue
                        model_name = protocol.product.model.name.short_name
                        assembly = queryset.filter(
                            workplace__type_of_work=1, product__model__name__short_name=model_name).count()
                        extract = queryset.filter(
                            workplace__type_of_work=2, product__model__name__short_name=model_name).count()
                        packaging = queryset.filter(
                            workplace__type_of_work=3, product__model__name__short_name=model_name).count()
                    elif group == 'variant_code':
                        if protocol.product.model.variant_code == variant_code:
                            continue
                        variant_code = protocol.product.model.variant_code
                        assembly = queryset.filter(
                            workplace__type_of_work=1, product__model__variant_code=variant_code).count()
                        extract = queryset.filter(
                            workplace__type_of_work=2, product__model__variant_code=variant_code).count()
                        packaging = queryset.filter(
                            workplace__type_of_work=3, product__model__variant_code=variant_code).count()
                    elif group == 'module':
                        if protocol.workplace.module.number == module:
                            continue
                        module = protocol.workplace.module.number
                        assembly = queryset.filter(
                            workplace__type_of_work=1, workplace__module__number=module).count()
                        extract = queryset.filter(
                            workplace__type_of_work=2, workplace__module__number=module).count()
                        packaging = queryset.filter(
                            workplace__type_of_work=3, workplace__module__number=module).count()
                    elif group == 'shift':
                        if protocol.shift == shift:
                            continue
                        shift = protocol.shift
                        assembly = queryset.filter(workplace__type_of_work=1, shift=shift).count()
                        extract = queryset.filter(workplace__type_of_work=2, shift=shift).count()
                        packaging = queryset.filter(workplace__type_of_work=3, shift=shift).count()
                else:
                    assembly = 0
                    extract = 0
                    packaging = 0
                    if protocol.workplace.type_of_work.id == 1:
                        assembly = 1
                    elif protocol.workplace.type_of_work.id == 2:
                        extract = 1
                    elif protocol.workplace.type_of_work.id == 3:
                        packaging = 1

                designation = ''
                if protocol.product.model.letter_part:
                    designation += protocol.product.model.letter_part
                if protocol.product.model.numeric_part:
                    designation += protocol.product.model.numeric_part
                if protocol.product.model.execution_part:
                    designation += protocol.product.model.execution_part

                res_list.append({
                    'model_name': protocol.product.model.name.short_name,
                    'variant_code': protocol.product.model.variant_code,
                    'module': protocol.workplace.module.number,
                    'designation': designation,
                    'assembly': assembly,
                    'extract': extract,
                    'packaging': packaging,
                    'shift': protocol.shift,
                })

            ordering = receive_serializer.validated_data['ordering']
            if ordering:
                if ordering == 'model_name':
                    res_list = sorted(res_list, key=lambda x: x['model_name'])
                if ordering == '-model_name':
                    res_list = sorted(res_list, key=lambda x: x['model_name'], reverse=True)
                if ordering == 'variant_code':
                    res_list = sorted(res_list, key=lambda x: x['variant_code'])
                if ordering == '-variant_code':
                    res_list = sorted(res_list, key=lambda x: x['variant_code'], reverse=True)
                if ordering == 'module':
                    res_list = sorted(res_list, key=lambda x: x['module'])
                if ordering == '-module':
                    res_list = sorted(res_list, key=lambda x: x['module'], reverse=True)
                if ordering == 'shift':
                    res_list = sorted(res_list, key=lambda x: x['shift'])
                if ordering == '-shift':
                    res_list = sorted(res_list, key=lambda x: x['shift'], reverse=True)
                if ordering == 'designation':
                    res_list = sorted(res_list, key=lambda x: x['designation'])
                if ordering == '-designation':
                    res_list = sorted(res_list, key=lambda x: x['designation'], reverse=True)

            paginator = StandartResultPaginator()
            page = paginator.paginate_queryset(res_list, request, view=self)
            res_serializer = DataForMainDocResponseSerializer(page, many=True)
            return paginator.get_paginated_response(res_serializer.data)

        return Response(receive_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
