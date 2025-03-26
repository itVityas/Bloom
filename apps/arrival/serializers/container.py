from django.db.models import Sum

from rest_framework import serializers
from apps.arrival.models import Container, Content
from apps.arrival.serializers.content import ContentSerializer, ContentMultySerializer
from apps.declaration.serializers.declaration import DeclarationSerializer


class ContainerFullSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model.
    This serializer includes the contents associated with the container.
    """
    contents = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Container
        fields = [
            'id',
            'name',
            'suppose_date',
            'load_date',
            'exit_date',
            'delivery',
            'location',
            'state',
            'count',
            'order',
            'notice',
            'contents',
        ]

    def get_contents(self, obj) -> list:
        """
        Returns the serialized contents for the container.

        :param obj: Container instance.
        :return: List of serialized content data.
        """
        contents = Content.objects.filter(container=obj)
        return ContentSerializer(contents, many=True).data

    def get_count(self, obj) -> int:
        """
        Returns the count of contents for the container.

        :return: Count of contents.
        """
        count = Content.objects.filter(container=obj).aggregate(total=Sum('count'))['total']
        return count if count else 0


class ContainerSetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model.
    This serializer is used for creating and updating Container instances.
    """

    class Meta:
        model = Container
        fields = "__all__"


class ContainerAndDeclarationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model including its associated declarations.
    """
    declarations = DeclarationSerializer(many=True, read_only=True)

    class Meta:
        model = Container
        fields = '__all__'


class ContainerBindSerializer(serializers.Serializer):
    """
    Serializer for binding containers to an order or unbinding them.

    If 'order_id' is null, containers will be unbound (order set to None).
    """
    order_id = serializers.IntegerField(required=False, allow_null=True)
    container_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )


class ContainerAndContantSetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model including its associated contents.
    """
    contents = ContentMultySerializer(many=True)

    class Meta:
        model = Container
        fields = '__all__'

    def create(self, validated_data):
        """
        Creates a new Container instance with associated contents.
        """
        contents_data = validated_data.pop('contents')
        container = Container.objects.create(**validated_data)
        for content_data in contents_data:
            Content.objects.create(container=container, **content_data)
        return container
