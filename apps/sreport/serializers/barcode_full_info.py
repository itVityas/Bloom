from rest_framework import serializers

from apps.warehouse.models import WarehouseDo, WarehouseTTN
from apps.warehouse.serializers.warehouse_action import WarehouseActionPostSerializer
from apps.warehouse.serializers.warehouse import WarehouseSerializer
from apps.account.serializers.user import UserSerializer
from apps.onec.serializers.onec_ttn import OneCTTNPostSerializer
from apps.shtrih.models import Protocols
from apps.shtrih.serializers.workplaces import WorkplacesSerializer
from apps.shtrih.serializers.user import ShtrihUserSerializer


class ProtocolReportSerializer(serializers.ModelSerializer):
    user = ShtrihUserSerializer(many=False, read_only=True)
    workplace = WorkplacesSerializer(many=False, read_only=True)

    class Meta:
        model = Protocols
        fields = '__all__'


class WarehouseTTNReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    warehouse = WarehouseSerializer(read_only=True, many=False)
    warehouse_action = WarehouseActionPostSerializer(read_only=True, many=False)
    onec_ttn = OneCTTNPostSerializer(read_only=True, many=False)

    class Meta:
        model = WarehouseTTN
        fields = '__all__'


class WarehouseDoReportSerializer(serializers.ModelSerializer):
    warehouse_ttn = WarehouseTTNReportSerializer(many=False)

    class Meta:
        model = WarehouseDo
        fields = '__all__'


class BarcodeInfoSerializer(serializers.Serializer):
    barcode = serializers.CharField(max_length=200)
    warehouse_do = serializers.SerializerMethodField()
    protocols = serializers.SerializerMethodField()

    def get_warehouse_do(self, obj) -> list:
        warehouse_do = WarehouseDo.objects.filter(product__barcode=obj['barcode'])
        if warehouse_do:
            serializer = WarehouseDoReportSerializer(warehouse_do, many=True)
            return serializer.data
        return None

    def get_protocols(self, obj) -> list:
        protocols = Protocols.objects.filter(product__barcode=obj['barcode'])
        if protocols:
            serializer = ProtocolReportSerializer(protocols, many=True)
            return serializer.data
        return None
