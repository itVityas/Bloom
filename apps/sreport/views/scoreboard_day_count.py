from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.sreport.models import ScoreboardDayCount
from apps.sreport.serializers.scoreboard_day_count import ScoreboardDayCountFullSerializer


@extend_schema(tags=['ProductPlan'])
@extend_schema_view(
    get=extend_schema(
        description="Get ScoreboardDayCount all data",
        responses={
            200: ScoreboardDayCountFullSerializer(many=True)
        }
    )
)
class ScoreboardDayCountView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ScoreboardDayCountFullSerializer
    queryset = ScoreboardDayCount.objects.all()

    def get(self, request):
        try:
            scoreboard = self.queryset
            return Response(ScoreboardDayCountFullSerializer(scoreboard, many=False).data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
