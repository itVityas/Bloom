import datetime

from rest_framework import serializers
from django.db.models import Sum

from apps.sreport.models import ScoreboardDayCount


class ScoreboardDayCountFullSerializer(serializers.Serializer):
    day_count = serializers.SerializerMethodField('get_day_count')
    month_count = serializers.SerializerMethodField('get_month_count')
    year_count = serializers.SerializerMethodField('get_year_count')

    class Meta:
        fields = [
            'day_count',
            'month_count',
            'year_count'
        ]

    def get_day_count(self, obj) -> int:
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        data = ScoreboardDayCount.objects.filter(
                work_date=today
            ).annotate(sum=Sum('quantity'))
        if data:
            total_sum = 0
            for i in data:
                total_sum += i.sum
            return total_sum
        return 0

    def get_month_count(self, obj) -> int:
        start_of_month = datetime.datetime.today().replace(day=1).strftime('%Y-%m-%d')
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        data = ScoreboardDayCount.objects.filter(
                work_date__gte=start_of_month,
                work_date__lte=today
            ).annotate(sum=Sum('quantity'))
        if data:
            total_sum = 0
            for i in data:
                total_sum += i.sum
            return total_sum
        return 0

    def get_year_count(self, obj) -> int:
        start_of_year = datetime.datetime.today().replace(month=1, day=1).strftime('%Y-%m-%d')
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        data = ScoreboardDayCount.objects.filter(
                work_date__gte=start_of_year,
                work_date__lte=today
            ).annotate(sum=Sum('quantity'))
        if data:
            total_sum = 0
            for i in data:
                total_sum += i.sum
            return total_sum
        return 0
