from rest_framework import serializers


class TtnItemSerializer(serializers.Serializer):
    name = serializers.CharField(
        help_text="name TTN",
        max_length=100
    )


class DocumentRequestSerializer(serializers.Serializer):
    document = serializers.CharField(
        help_text="Number of document",
        max_length=50
    )
    ttn = TtnItemSerializer(
        many=True,
        help_text="List of TTN"
    )
