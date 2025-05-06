from rest_framework import serializers

from apps.general.models import AddTitle, AddBody
from apps.general.serializers.add_body import AddBodySerializer


class AddTitleSerializer(serializers.ModelSerializer):
    body = AddBodySerializer(many=True, read_only=True)

    class Meta:
        model = AddTitle
        fields = '__all__'


class AddTitleGetSerializer(serializers.ModelSerializer):
    bodies = serializers.SerializerMethodField()

    class Meta:
        model = AddTitle
        fields = '__all__'

    def get_bodies(self, obj) -> dict:
        return AddBodySerializer(AddBody.objects.filter(title=obj), many=True).data
