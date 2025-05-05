from rest_framework import serializers

from apps.general.models import AddBody


class AddBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddBody
        fields = '__all__'
