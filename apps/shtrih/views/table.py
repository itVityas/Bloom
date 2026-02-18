from datetime import date, datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Sum
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.shtrih.models import ScoreboardView
from apps.shtrih.serializers.scorevoard import ScoreboardSerializer


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get table data',
        parameters=[
            OpenApiParameter(
                name='start_date',
                location=OpenApiParameter.QUERY,
                description='start_date',
                required=False,
                type=date,
            ),
            OpenApiParameter(
                name='end_date',
                location=OpenApiParameter.QUERY,
                description='end_date',
                required=False,
                type=date,
            ),
        ],
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
        try:
            date_time = datetime.today()
            end_date = request.query_params.get('end_date', None)
            start_date = request.query_params.get('start_date', None)
            if not end_date:
                today = date.today()
            else:
                today = date.fromisoformat(end_date)
            if not start_date:
                first_day = today.replace(day=1)
            else:
                first_day = date.fromisoformat(start_date)
            scoreboard = ScoreboardView.objects.filter(work_date=today)
            scoreboard_month = ScoreboardView.objects.filter(
                work_date__range=(first_day, today)
                ).values('module_digit', 'workplace', 'shift').annotate(month_quantity=Sum('quantity'))
            data_month = []
            for i in scoreboard_month:
                today_quantity = 0
                for day in scoreboard:
                    if day.module_digit == i.get('module_digit') \
                            and day.workplace == i.get('workplace') and day.shift == i.get('shift'):
                        today_quantity = day.quantity
                data_month.append({
                    'module': i.get('module_digit'),
                    'month': i.get('month_quantity'),
                    'workplace': i.get('workplace'),
                    'shift': i.get('shift'),
                    'today': today_quantity,
                })
            return Response({'scoretable': data_month, 'date': date_time})
        except Exception as ex:
            return Response({'error': str(ex)})
