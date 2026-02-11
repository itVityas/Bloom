from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Sum
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.shtrih.models import ScoreboardView
from apps.shtrih.serializers.scorevoard import ScoreboardSerializer


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get table data',
        description='''Get data for table
{
    "today": [
        {
            "quantity": 925,
            "shift": "A",
            "module_digit": 1,
            "work_date": "2026-02-09"
        },
        {
            "quantity": 490,
            "shift": "B",
            "module_digit": 1,
            "work_date": "2026-02-09"
        },
        {
            "quantity": 832,
            "shift": "A",
            "module_digit": 3,
            "work_date": "2026-02-09"
        },
        {
            "quantity": 113,
            "shift": "A",
            "module_digit": 4,
            "work_date": "2026-02-09"
        }
    ],
    "month": [
        {
            "1": 15581
        },
        {
            "2": 12324
        },
        {
            "3": 12450
        },
        {
            "4": 3081
        }
    ]
}
'''
    )
)
class TableDataView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ScoreboardSerializer
    quantity = ScoreboardView.objects.all()

    def get(self, request):
        today = date.today()
        first_day = today.replace(day=1)
        scoreboard = ScoreboardView.objects.filter(work_date=today)
        data_today = ScoreboardSerializer(scoreboard, many=True).data
        scoreboard_month = ScoreboardView.objects.filter(
            work_date__range=(first_day, today)
            ).values('module_digit').annotate(month_quantity=Sum('quantity'))
        data_month = []
        for i in scoreboard_month:
            data_month.append({
                i.get('module_digit'): i.get('month_quantity')
            })
        return Response({'today': data_today, 'month': data_month})
