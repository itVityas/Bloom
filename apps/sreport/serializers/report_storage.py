from rest_framework import serializers


from apps.sreport.models import ReportStorage


class ReportStorageSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    warehouse_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = ReportStorage
        fields = '__all__'

    def get_total(self, obj) -> int:
        if isinstance(obj, dict):
            return obj.get('uncleared', 0) + obj.get('cleared', 0) + obj.get('simple', 0)
        return obj.uncleared + obj.cleared + obj.simple

# class ReportStorageSerializer(serializers.Serializer):
#     """
#     model_name = Имя модели
#     uncleared = нерасстоможенные
#     cleared = растоможенные
#     simple = простые (product_transition.new_product)
#     total = сумма трех
#     compensation = product (invoices.recitiont_id=4)
#     """
#     model_name = serializers.CharField()
#     model_name_id = serializers.IntegerField()
#     uncleared = serializers.IntegerField()
#     cleared = serializers.IntegerField()
#     simple = serializers.IntegerField()
#     total = serializers.IntegerField()
#     compensation = serializers.IntegerField()
