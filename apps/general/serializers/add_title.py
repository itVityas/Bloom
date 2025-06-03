from rest_framework import serializers

from apps.general.models import AddTitle, AddBody
from apps.general.serializers.add_body import AddBodySerializer


class AddTitleSerializer(serializers.ModelSerializer):
    """
    Serializer for AddTitle model with nested content.

    Features:
    - Nested serialization of related content
    - Read-only content field
    - Explicit field definitions
    - Optimized database queries
    """
    body = AddBodySerializer(many=True, read_only=True)

    class Meta:
        model = AddTitle
        fields = '__all__'


class AddTitleGetSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing titles with associated content counts.

    Features:
    - Content count instead of full content list
    - Optimized for list views
    - Minimal data transfer
    """
    bodies = serializers.SerializerMethodField()

    class Meta:
        model = AddTitle
        fields = '__all__'

    def get_bodies(self, obj) -> dict:
        return AddBodySerializer(AddBody.objects.filter(title=obj), many=True).data
