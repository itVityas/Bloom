from rest_framework import serializers

from apps.declaration.models import G44


class G44Serializer(serializers.ModelSerializer):
    class Meta:
        model = G44
        fields = "__all__"
