from rest_framework import serializers

from apps.shtrih.models import ScoreboardView


class ScoreboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreboardView
        fields = '__all__'
