from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.sreport.serializers.name_count import ModelNameCountSerializer


@extend_schema(tags=['Warehouse report'])
@extend_schema_view(
    post=extend_schema(
        description='Report from model name uncleared and decl count',
        responses={200: ModelNameCountSerializer},
        methods=["POST"],
    )
)
class ModelNameCountView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ModelNameCountSerializer

    def post(self, request):
        try:
            serializer = ModelNameCountSerializer(data=request.data, many=False)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
