from rest_framework import serializers

from apps.arrival.models import MakeUp


class MakeUpPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakeUp
        fields = [
            'lot',
            'file'
        ]

    def create(self, validated_data):
        return self._check_save(validated_data)

    def update(self, instance, validated_data):
        return self._check_save(validated_data, instance)

    def _check_save(self, validated_date, instance=None):
        """Check save MakeUp model."""
        inst_file = None
        inst_lot = None
        if instance:
            inst_file = instance.file
            inst_lot = instance.lot
        file = validated_date.get('file', inst_file)
        lot = validated_date.get('lot', inst_lot)
        if not file or not lot:
            raise serializers.ValidationError('File and order are required')

        makeup = MakeUp.objects.filter(lot=lot).first()
        if makeup:
            makeup.file = file
            makeup.filename = file.name
            makeup.save()
            return makeup
        if instance:
            instance.file = file
            instance.filename = file.name
            instance.save()
            return instance
        return MakeUp.objects.create(lot=lot, file=file, filename=file.name)


class MakeUpGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakeUp
        fields = '__all__'
