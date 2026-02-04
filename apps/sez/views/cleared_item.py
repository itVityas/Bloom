import logging

from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Sum, F

from apps.sez.models import ClearedItem
from apps.sez.permissions import ClearedItemPermission
from apps.sez.serializers.cleared_item import ClearedItemSerializer, ClearedItemAssemblySerializer
from apps.sez.serializers.cleared_item_by_clearance import ClearedItemListSerializer
from apps.sez.filterset import ClearedItemFilter
from apps.declaration.models import DeclaredItem
from Bloom.paginator import StandartResultPaginator


logger = logging.getLogger('apps.omega')


@extend_schema(tags=['ClearedItem'])
@extend_schema_view(
    get=extend_schema(
        summary='List all cleared items',
        description='Permission: admin, arrival_reader, cleared_item_writer',
    ),
)
class ListClearedItemView(ListAPIView):
    permission_classes = [IsAuthenticated, ClearedItemPermission]
    serializer_class = ClearedItemSerializer
    queryset = ClearedItem.objects.all()
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClearedItemFilter


@extend_schema(tags=['ClearedItem'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a cleared item',
        description='Permission: admin, cleared_item_writer',
        responses=ClearedItemListSerializer,
    ),
)
class CreateClearedItemView(CreateAPIView):
    permission_classes = [IsAuthenticated, ClearedItemPermission]
    serializer_class = ClearedItemSerializer
    queryset = ClearedItem.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                declaration_item = DeclaredItem.objects.filter(
                    id=serializer.validated_data['declared_item_id'].id
                ).first()
                if not declaration_item:
                    return Response({'error': 'Не найден элемент декларации'}, status=status.HTTP_400_BAD_REQUEST)
                if declaration_item.available_quantity < serializer.validated_data['quantity']:
                    return Response(
                        {'error': f'Недостаточное количество товара {serializer.validated_data["quantity"]},' +
                            f'в наличии {declaration_item.available_quantity}'},
                        status=status.HTTP_400_BAD_REQUEST)
                serializer.validated_data['is_hand'] = True
                serializer.save()
                declaration_item.available_quantity -= serializer.validated_data['quantity']
                declaration_item.save()
                logger.info(f'Creating cleared item: {request.data}')
                serializer = ClearedItemListSerializer(instance=serializer.instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f'Error creating cleared item: {e}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['ClearedItem'])
@extend_schema_view(
    delete=extend_schema(
        summary='Create a cleared item',
        description='Permission: admin, cleared_item_writer',
    ),
)
class DestroyClearedItemView(DestroyAPIView):
    permission_classes = [IsAuthenticated, ClearedItemPermission]
    serializer_class = ClearedItemSerializer
    queryset = ClearedItem.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                declaration_item = DeclaredItem.objects.filter(
                    id=instance.declared_item_id.id
                ).first()
                if not declaration_item:
                    return Response({'error': 'Не найден элемент декларации'}, status=status.HTTP_400_BAD_REQUEST)
                declaration_item.available_quantity += instance.quantity
                declaration_item.save()
                logger.info(f'Deleting cleared item: {instance.id}')
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f'Error deleting cleared item: {e}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['ClearedItem'])
@extend_schema_view(
    patch=extend_schema(
        summary='Partial update the cleared item',
        description='''
        Permission: admin, cleared_item_writer;
        Обновляет только поле quantity, и изменяя available_quantity в declared_item''',
    ),
    put=extend_schema(
        summary='Full update the cleared item',
        description='''
        Permission: admin, cleared_item_writer;
        Обновляет только поле quantity, и изменяя available_quantity в declared_item''',
    ),
)
class UpdateClearedItemView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ClearedItemPermission]
    serializer_class = ClearedItemSerializer
    queryset = ClearedItem.objects.all()

    def patch(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                instanse = self.get_object()
                if serializer.is_valid(raise_exception=True):
                    if serializer.validated_data['quantity'] <= 0:
                        return Response({'error': 'Количество не может быть меньше 0'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    dif = instanse.quantity - serializer.validated_data['quantity']
                    if instanse.declared_item_id.available_quantity + dif < 0:
                        return Response(
                            {'error': f'Недостаточное количество товара на складе {
                                instanse.declared_item_id.available_quantity}'},
                            status=status.HTTP_400_BAD_REQUEST)
                instanse.quantity = serializer.validated_data['quantity']
                instanse.declared_item_id.available_quantity += dif
                instanse.is_hand = True
                instanse.declared_item_id.save()
                instanse.save()

                if not instanse.declared_item_id:
                    return Response({'error': 'Не найден элемент декларации'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(ClearedItemListSerializer(instanse).data, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                instanse = self.get_object()
                if serializer.is_valid(raise_exception=True):
                    if serializer.validated_data['quantity'] <= 0:
                        return Response({'error': 'Количество не может быть меньше 0'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    dif = instanse.quantity - serializer.validated_data['quantity']
                    if instanse.declared_item_id.available_quantity + dif < 0:
                        return Response(
                            {'error': f'Недостаточное количество товара на складе {
                                instanse.declared_item_id.available_quantity}'},
                            status=status.HTTP_400_BAD_REQUEST)
                instanse.quantity = serializer.validated_data['quantity']
                instanse.declared_item_id.available_quantity += dif
                instanse.is_hand = True
                instanse.declared_item_id.save()
                instanse.save()

                if not instanse.declared_item_id:
                    return Response({'error': 'Не найден элемент декларации'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(ClearedItemListSerializer(instanse).data, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['ClearedItem'])
@extend_schema_view(
    get=extend_schema(
        summary='List all cleared items with assembling',
        description='Permission: admin, arrival_reader, cleared_item_writer',
    ),
)
class ClearedItemListAssemblingView(ListAPIView):
    permission_classes = [IsAuthenticated, ClearedItemPermission]
    serializer_class = ClearedItemAssemblySerializer
    queryset = ClearedItem.objects.all()
    pagination_class = StandartResultPaginator

    def list(self, request, pk: int, *args, **kwargs):
        queryset = ClearedItem.objects.filter(clearance_invoice_items__clearance_invoice=pk).values(
            model_name=F('clearance_invoice_items__model_name_id__name'),
            name=F('declared_item_id__name'),
            code_1c=F('declared_item_id__item_code_1c')
            ).annotate(
                total_quantity=Sum('quantity')
            ).values(
                'model_name', 'total_quantity', 'name', 'code_1c'
            ).order_by('name')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
