from rest_framework import serializers


class ReportStorageSerializer(serializers.Serializer):
    """
    model_name = Имя модели
    uncleared = нерасстоможенные
    cleared = растоможенные
    simple = простые (product_transition.new_product)
    total = сумма трех
    compensation = product (invoices.recitiont_id=4)
    """
    model_name = serializers.CharField()
    uncleared = serializers.IntegerField()
    cleared = serializers.IntegerField()
    simple = serializers.IntegerField()
    total = serializers.IntegerField()
    compensation = serializers.IntegerField()
