from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiExample, OpenApiResponse)
from rest_framework.response import Response
from rest_framework import status

from apps.sgp.serializers.consignment import ConsignmentSerializer


@extend_schema(tags=['Consignment'])
@extend_schema_view(
    post=extend_schema(
        summary='Create consignment',
        description='''
        isAdmin
        Key fields:
        - document_number: Unique document identifier (20 chars max)
        - doc_date: Date as integer timestamp (YYYYMMDD format)
        - recipient: Recipient name (250 chars max)
        - recipient_code: Recipient identifier (7 chars max)
        - quantity: Item quantity (positive number)
        - unp: Taxpayer Identification Number (20 chars max)

        Optional fields:
        - article: Article number/SKU (25 chars max)
        - invoice_number: Reference invoice number (20 chars max)
        - invoice_series: Invoice series identifier (4 chars max)
        - gtin: Global Trade Item Number (14 digits)
        ''',
        request=ConsignmentSerializer(many=True),
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=ConsignmentSerializer,
                description='Consignment records successfully created',
                examples=[
                    OpenApiExample(
                        'Success Example',
                        value=[
                            {
                                "document_number": "DOC12345",
                                "doc_date": 20231231,
                                "recipient": "Company XYZ",
                                "recipient_code": "RC12345",
                                "quantity": 10.5,
                                "unp": "123456789",
                                "article": "ART-001"
                            }
                        ]
                    )
                ]
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Invalid input data',
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        value={
                            "doc_date": ["Invalid date format. Use YYYYMMDD"],
                            "quantity": ["Must be a positive number"]
                        }
                    )
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description='Authentication credentials were not provided'
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description='User does not have admin privileges'
            )
        },
    ),
)
class ConsignmentCreateView(APIView):
    """
    API endpoint for creating consignment records.

    Supports both single and bulk creation of consignments.
    Requires admin privileges for all operations.
    """
    serializer_class = ConsignmentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ConsignmentSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
