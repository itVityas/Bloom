import logging

from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from apps.sez.models import ClearedItem
from apps.sez.permissions import ClearedItemPermission
from apps.sez.serializers.cleared_item import ClearedItemSerializer
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
