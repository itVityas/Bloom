from rest_framework import serializers

from apps.arrival.models import Container, Content
from apps.arrival.serializers.content import ContentSerializer


class ContainerFullSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model.
    This serializer includes the content associated with the container.
    """
    contents = serializers.SerializerMethodField()

    class Meta:
        model = Container
        fields = [
            'id',
            'name',
            'suppose_date',
            'exit_date',
            'delivery',
            'location',
            'state',
            'invoice',
            'contents',
        ]

    def get_contents(self, obj) -> dict:
        contents = Content.objects.filter(container=obj)
        return ContentSerializer(contents, many=True).data


class ContainerSetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model.
    This serializer is used for creating and updating Container instances.
    """
    class Meta:
        model = Container
        fields = "__all__"
