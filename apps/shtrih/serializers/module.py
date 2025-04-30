from rest_framework import serializers

from apps.shtrih.models import Modules


class ModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = '__all__'
