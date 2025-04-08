from rest_framework import serializers

from apps.sez.models import ClearedItem
from apps.shtrih.models import Products


class DocumentClearedItemSerializer(serializers.ModelSerializer):
    declaration_number = serializers.CharField(read_only=True, required=False)
    declaration_date = serializers.CharField(read_only=True, required=False)
    amount = serializers.IntegerField(read_only=True, required=False)
    unit = serializers.CharField(read_only=True, required=False)
    cost = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = ClearedItem
        fields = [
            'id',
            'product_id',
            'declaration_number',
            'declaration_date',
            'amount',
            'unit',
            'cost',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # declaration = instance.declared_item_id.declaration
        # data['declaration_number'] = declaration.declaration_number
        # data['declaration_date'] = declaration.declaration_date
        product = Products.objects.filter(id=instance.product_id)
        if product.exists() and product.first().consignment:
            product = product.first()
            data['declaration_number'] = product.consignment.declaration_number
            data['declaration_date'] = product.consignment.declaration_date.strftime("%Y.%m.%d")
        else:
            data['declaration_number'] = None
            data['declaration_date'] = None
        data['amount'] = 0
        data['unit'] = 'test'
        data['cost'] = 0
        return data
