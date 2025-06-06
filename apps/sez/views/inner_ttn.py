from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView,
    RetrieveUpdateDestroyAPIView)
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiResponse)
from django.http import HttpResponse
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.sez.models import InnerTTN, InnerTTNItems
from apps.shtrih.models import ModelNames
from apps.sez.serializers.inner_ttn import InnerTTNSerializer, InnerTTNPostSerializer
from apps.sez.permissions import InnerTTNPermission
from apps.sez.services.inner_ttn_pdf import get_ttn_pdf
from Bloom.paginator import StandartResultPaginator
from apps.sez.filterset import InnerTTNFilter


@extend_schema(tags=['InnerTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='get list Inner TTN',
        description='Permission: admin, stz_reader, stz, ttn'
    )
)
class InnerTTNListView(ListAPIView):
    permission_classes = (IsAuthenticated, InnerTTNPermission)
    serializer_class = InnerTTNSerializer
    queryset = InnerTTN.objects.all()
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = InnerTTNFilter


@extend_schema(tags=['InnerTTN'])
@extend_schema_view(
    post=extend_schema(
        summary='create Inner TTN',
        description='Permission: admin, stz, ttn',
        responses={
            200: OpenApiResponse(description="PDF file"),
            400: OpenApiResponse(description="Wrong request"),
        }
    ),
)
class InnerTTNCreateView(CreateAPIView):
    """
{
  "shipper_unp": "string",
  "consignee_unp": "string",
  "customer_unp": "string",
  "customer": "string",
  "shipper": "string",
  "consignee": "string",
  "document": "string",
  "load": "string",
  "unload": "string",
  "date": "2025-05-14",
  "notice": "string",
  "items": [
    {
        "item_name": "item1",
        "measure": "шт",
        "quantity": 10,
        "price_pcs": 123,
        "weight": 234
    },
    {
        "item_name": "item2",
        "measure": "шт",
        "quantity": 10,
        "price_pcs": 10,
        "weight": 20
    }
  ]
}
    """
    permission_classes = (IsAuthenticated, InnerTTNPermission)
    serializer_class = InnerTTNSerializer
    queryset = InnerTTN.objects.all()

    def post(self, request):
        items = request.data.pop('items', None)

        try:
            ttn = InnerTTN.objects.create(**request.data)
            if items:
                for item in items:
                    model_name_id = item.pop('model_name', None)
                    model_name = ModelNames.objects.filter(id=model_name_id).first()
                    if model_name:
                        InnerTTNItems.objects.create(inner_ttn=ttn, model_name=model_name, **item)
        except Exception as ex:
            return HttpResponse(ex, status=400)

        return Response(InnerTTNSerializer(ttn).data, status=200)


@extend_schema(tags=['InnerTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='get inner ttn pdf by id',
        description='Permission: admin, stz_reader, stz, ttn',
        responses={
            200: OpenApiResponse(description="PDF file"),
            400: OpenApiResponse(description="Wrong request"),
        }
    ),
)
class InnerTTNPDFView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, InnerTTNPermission)
    serializer_class = InnerTTNSerializer
    queryset = InnerTTN.objects.all()

    def get(self, request, pk):
        file_path = get_ttn_pdf(pk)
        if not file_path:
            return HttpResponse('Не удалось сформировать PDF файл', status=400)

        document = open(file_path, 'rb')
        file_name = file_path.split('/')[1]
        response = HttpResponse(document, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response


@extend_schema(tags=["InnerTTN"])
@extend_schema_view(
    get=extend_schema(
        summary='get inner ttn by id',
        description='Permission: admin, stz_reader, stz, ttn',
    )
)
class InnerTTNDetailedView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, InnerTTNPermission)
    serializer_class = InnerTTNSerializer
    queryset = InnerTTN.objects.all()


@extend_schema(tags=["InnerTTN"])
@extend_schema_view(
    get=extend_schema(
        summary='get inner ttn by uuid',
        description='Permission: admin, stz_reader, stz, ttn',
    )
)
class InnerTTNDetailedByUUIDView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, InnerTTNPermission)
    serializer_class = InnerTTNSerializer
    queryset = InnerTTN.objects.all()

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        return InnerTTN.objects.filter(uuid=uuid).first()


@extend_schema(tags=["InnerTTN"])
@extend_schema_view(
    get=extend_schema(
        summary='delete inner ttn by id',
        description='Permission: admin, stz_reader, stz, ttn',
    ),
    put=extend_schema(
        summary='full update inner ttn by id',
        description='Permission: admin, stz, ttn',
    ),
    patch=extend_schema(
        summary='partial update inner ttn by id',
        description='Permission: admin, stz, ttn',
    ),
    delete=extend_schema(
        summary='delete inner ttn by id',
        description='Permission: admin, stz, ttn',
    )
)
class InnerTTNStandardUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, InnerTTNPermission)
    serializer_class = InnerTTNPostSerializer
    queryset = InnerTTN.objects.all()
