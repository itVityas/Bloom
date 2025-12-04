from rest_framework import serializers

from apps.omega.models import OBJ_ATTR_VALUES_1000004


class ObjAttrValues1000004Serializer(serializers.ModelSerializer):
    class Meta:
        model = OBJ_ATTR_VALUES_1000004
        fields = '__all__'
