from django.db.models import Sum

from rest_framework import serializers
from apps.arrival.models import Container, Content, Order
from apps.arrival.serializers.content import ContentSerializer, ContentMultySerializer
from apps.declaration.serializers.declaration import DeclarationSerializer
from apps.arrival.serializers.lot import LotPostSerializer
from apps.invoice.models import TrainDoc, InvoiceContainer
from apps.invoice.utils.check_excel import find_sheet
from apps.arrival.exceptions import DuplicateContainerException


class InvoiceContainerSerializer(serializers.ModelSerializer):
    """
    Basic serializer for the Invoice model.
    This serializer includes all fields of the Invoice model without nested data.
    """
    class Meta:
        model = InvoiceContainer
        fields = '__all__'


class OrderSmallSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    This serializer includes only the 'id' and 'name' fields of the Order model.
    """
    class Meta:
        model = Order
        fields = ['id', 'name']


class ContainerAndOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model including its associated order.
    """
    order = OrderSmallSerializer(read_only=True)

    class Meta:
        model = Container
        fields = '__all__'


class ContainerFullSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model.
    This serializer includes the contents associated with the container.
    """
    contents = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    invoice_container = serializers.SerializerMethodField()

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
            'invoice_container',
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

    def get_invoice_container(self, obj) -> dict:
        """
        Returns whether the container has an invoice.

        :return: True if the container has an invoice, False otherwise.
        """
        invoice = InvoiceContainer.objects.filter(container=obj).first()
        if not invoice:
            return {}
        return InvoiceContainerSerializer(invoice).data


class ContainerLotFullSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model.
    This serializer includes the contents associated with the container.
    """
    contents = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    invoice_container = serializers.SerializerMethodField()
    lot = LotPostSerializer(read_only=True)

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
            'invoice_container',
            'lot',
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

    def get_invoice_container(self, obj) -> dict:
        """
        Returns whether the container has an invoice.

        :return: True if the container has an invoice, False otherwise.
        """
        invoice = InvoiceContainer.objects.filter(container=obj).first()
        if not invoice:
            return {}
        return InvoiceContainerSerializer(invoice).data


class ContainerSetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model.
    This serializer is used for creating and updating Container instances.
    """

    class Meta:
        model = Container
        fields = "__all__"

    def validate(self, attrs):
        container_name = attrs.get('name', None)
        order = attrs.get('order', None)
        lot = attrs.get('lot', None)
        if container_name and order and lot:
            if Container.objects.filter(name=container_name, order=order, lot=lot).first():
                raise DuplicateContainerException(container_name=container_name)
        elif order:
            if Container.objects.filter(name=container_name, order=order).first():
                raise DuplicateContainerException(container_name=container_name)
        elif lot:
            if Container.objects.filter(name=container_name, lot=lot).first():
                raise DuplicateContainerException(container_name=container_name)
        return super().validate(attrs)

    def update(self, instance, validated_data):
        name = validated_data.get('name', None)
        lot = validated_data.get('lot', None)
        if lot or name:
            try:
                invoices = InvoiceContainer.objects.filter(container=instance)
                traindoc = TrainDoc.objects.filter(lot=lot).first()
                for inv in invoices:
                    if traindoc:
                        inv.sheet = find_sheet(
                            invoice_number=inv.number,
                            container_name=name,
                            file=traindoc.file
                        )
                        inv.save()
                    inv.sheet = None
                    inv.save()
            except Exception as e:
                print(e)
        return super().update(instance, validated_data)


class ContainerAndDeclarationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Container model including its associated declarations.
    """
    declarations = DeclarationSerializer(many=True, read_only=True)
    count = serializers.SerializerMethodField()
    invoice_container = serializers.SerializerMethodField()
    lot = LotPostSerializer(read_only=True)

    class Meta:
        model = Container
        fields = '__all__'

    def get_count(self, obj) -> int:
        """
        Returns the count of contents for the container.

        :return: Count of contents.
        """
        count = Content.objects.filter(container=obj).aggregate(total=Sum('count'))['total']
        return count if count else 0

    def get_invoice_container(self, obj) -> dict:
        """
        Returns whether the container has an invoice.

        :return: True if the container has an invoice, False otherwise.
        """
        invoice = InvoiceContainer.objects.filter(container=obj).first()
        if not invoice:
            return {}
        return InvoiceContainerSerializer(invoice).data


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


class ContainerMassUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for mass updating the state of containers.
    """
    class Meta:
        model = Container
        fields = [
            'id',
            'state',
            'location',
            'suppose_date',
        ]
