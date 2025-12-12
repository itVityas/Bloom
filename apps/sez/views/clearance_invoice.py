from datetime import datetime

from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView, ListAPIView, CreateAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from apps.sez.models import ClearanceInvoice, ClearanceInvoiceItems
from apps.shtrih.models import ModelNames
from apps.sez.permissions import ClearanceInvoicePermission
from apps.sez.serializers.clearance_invoice import (
    ClearanceInvoiceSerializer,
    FullClearanceInvoiceSerializer,
    ClearanceInvoiceListSerializer,
    ClearanceInvoiceEmptySerializer)
from Bloom.paginator import StandartResultPaginator
from apps.sez.filterset import ClearanceInvoiceFilter
from rest_framework import status
from rest_framework.response import Response


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    get=extend_schema(
        summary='List all clearance invoices',
        description='Permission: admin, stz_reader, clearance_invoice_writer',
    ),
)
class ClearanceInvoiceListAPIView(ListAPIView):
    """
    List all clearance invoices or create a new clearance invoice.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = ClearanceInvoiceListSerializer
    queryset = ClearanceInvoice.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_class = ClearanceInvoiceFilter
    pagination_class = StandartResultPaginator


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a clearance invoice',
        description='Permission: admin, clearance_invoice_writer',
    ),
)
class ClearanceInvoiceCreateAPIView(CreateAPIView):
    """
    List all clearance invoices or create a new clearance invoice.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = ClearanceInvoiceSerializer
    queryset = ClearanceInvoice.objects.all()


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve clearance invoice by ID',
        description='Permission: admin, stz_reader, clearance_invoice_writer',
    ),
    put=extend_schema(
        summary='Update clearance invoice',
        description='Permission: admin, clearance_invoice_writer',
    ),
    patch=extend_schema(
        summary='Partial update clearance invoice',
        description='Permission: admin, clearance_invoice_writer',
    ),
    delete=extend_schema(
        summary='Delete clearance invoice',
        description='Permission: admin, clearance_invoice_writer',
    ),
)
class ClearanceInvoiceDetailedView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a clearance invoice.
    """
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = ClearanceInvoiceSerializer
    queryset = ClearanceInvoice.objects.all()


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    get=extend_schema(
        summary='Get full clearance invoice',
        description='Permission: admin, stz_reader, clearance_invoice_writer',
    )
)
class GetFullClearanceInvoiceView(RetrieveAPIView):
    """
    Get ClearanceInvoice + ClearanceInvoiceItem
    """
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = FullClearanceInvoiceSerializer
    queryset = ClearanceInvoice.objects.all()


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    get=extend_schema(
        summary='List all clearance invoices + items',
        description='Permission: admin, stz_reader, clearance_invoice_writer',
    ),
)
class GetFullClearancesInvoiceListView(ListAPIView):
    """
    Get ClearanceInvoice + ClearanceInvoiceItem
    """
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = FullClearanceInvoiceSerializer
    queryset = ClearanceInvoice.objects.all()
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend,]
    filterset_class = ClearanceInvoiceFilter


@extend_schema(tags=['ClearanceInvoice'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a clearance invoice with Empty ClearanceIncoiceItem',
        description='Permission: admin, clearance_invoice_writer',
        responses=FullClearanceInvoiceSerializer,
    ),
)
class CreateClearanceInvoiceEmtpyView(CreateAPIView):
    """
    Create a clearance invoice with Empty ClearanceIncoiceItem
    """
    permission_classes = (IsAuthenticated, ClearanceInvoicePermission)
    serializer_class = ClearanceInvoiceEmptySerializer
    queryset = ClearanceInvoice.objects.all()

    def create(self, request, *args, **kwargs):
        clearance_invoice = ClearanceInvoice(
            count=request.data.get('count', 1),
            cleared=True,
            ttn='R0',
            responsible=request.user,
            recipient='Вывоз',
            create_at=datetime.now(tz=timezone.get_current_timezone()),
            date_payments=datetime.now(tz=timezone.get_current_timezone()),
            date_calc=datetime.now(tz=timezone.get_current_timezone()),
            is_gifted=request.data.get('is_gifted'),
            only_panel=False,
        )
        clearance_invoice.save()
        clearance_invoice_item = ClearanceInvoiceItems(
            clearance_invoice=clearance_invoice,
            model_name_id=ModelNames.objects.get(id=589),
            quantity=1,
        )
        clearance_invoice_item.save()
        serializer = FullClearanceInvoiceSerializer(clearance_invoice)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
