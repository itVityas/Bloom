from rest_framework import serializers


from apps.declaration.models import DeclaredItem, Declaration


class DeclarationThisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaration
        fields = '__all__'


class DeclaredItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclaredItem
        fields = '__all__'


class DeclarationItemGetSerializer(serializers.ModelSerializer):
    declaration = DeclarationThisSerializer(read_only=True)

    class Meta:
        model = DeclaredItem
        fields = '__all__'


class DeclaredItemFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
