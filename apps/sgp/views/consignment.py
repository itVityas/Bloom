from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework import status

from apps.sgp.serializers.consignment import ConsignmentSerializer


@extend_schema(tags=['Consignment'])
@extend_schema_view(
    post=extend_schema(
        summary='Create consignment',
        description='''
        isAdmin
    document_number = CharField(max_length=20)
    doc_date = Integer (timestamp)
    recipient = CharField(max_length=250)
    recipient_code = CharField(max_length=7)
    quantity = FloatField()
    article = CharField(max_length=25, blank=True, null=true)
    invoice_number = CharField(max_length=20,
        required=False, blank=True, null=true)
    invoice_series = CharField(max_length=4,
        required=False, blank=True, null=True)
    unp = CharField(max_length=20)
    gtin = CharField(max_length=14, required=False, blank=True, null=True)
        '''
    ),
)
class ConsignmentCreateView(APIView):
    serializer_class = ConsignmentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ConsignmentSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
