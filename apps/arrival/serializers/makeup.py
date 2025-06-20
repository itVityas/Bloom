from rest_framework import serializers

from apps.arrival.models import MakeUp


class MakeUpPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakeUp
        fields = [
            'order',
            'file',
        ]

    def create(self, validated_data):
        # return self._check_save(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # return self._check_save(validated_data, instance)
        return super().update(instance, validated_data)

    def _check_save(self, validated_date, instance=None):
        """Check save MakeUp model. Now not used. Use if we need check 1 order - 1 makeup"""
        inst_file1 = None
        inst_file2 = None
        inst_order = None
        if instance:
            inst_file1 = instance.file1
            inst_file2 = instance.file2
            inst_order = instance.lot
        file1 = validated_date.get('file1', inst_file1)
        file2 = validated_date.get('file2', inst_file2)
        order = validated_date.get('order', inst_order)
        if not file1 or not order:
            raise serializers.ValidationError('File and order are required')

        makeup = MakeUp.objects.filter(order=order).first()
        if makeup:
            makeup.file1 = file1
            if file2:
                makeup.file2 = file2
                makeup.filename2 = file2.name
            makeup.filename1 = file1.name
            makeup.save()
            return makeup
        if instance:
            instance.file1 = file1
            instance.filename1 = file1.name
            if file2:
                instance.file2 = file2
                instance.filename2 = file2.name
            instance.save()
            return instance
        if not file2:
            filename2 = None
        else:
            filename2 = file2.name
        return MakeUp.objects.create(
            order=order,
            file1=file1,
            filename1=file1.name,
            file2=file2,
            filename2=filename2,
        )


class MakeUpGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakeUp
        fields = '__all__'
