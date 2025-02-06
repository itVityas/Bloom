from rest_framework import serializers

from apps.arrival.models import Content


class ContentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Content model.
    This serializer is used for all Content instances.
    """
    class Meta:
        model = Content
        fields = "__all__"
