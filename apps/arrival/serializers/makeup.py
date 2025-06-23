from rest_framework import serializers

from apps.arrival.models import MakeUp


class MakeUpPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakeUp
        fields = [
            'order',
            'file',
            'note',
        ]

    def create(self, validated_data):
        return self._check_save(validated_data)

    def update(self, instance, validated_data):
        return self._check_save(validated_data, instance)

    def _check_save(self, validated_date, instance=None):
        """Check save MakeUp model."""
        inst_file = None
        inst_order = None
        inst_note = None
        if instance:
            inst_file = instance.file
            inst_order = instance.order
            inst_note = instance.note
        file = validated_date.get('file', inst_file)
        order = validated_date.get('order', inst_order)
        note = validated_date.get('note', inst_note)

        if not file or not order:
            raise serializers.ValidationError('File and order are required')

        # makeup = MakeUp.objects.filter(order=order).first()
        # if makeup:
        #     makeup.file1 = file1
        #     if file2:
        #         makeup.file2 = file2
        #         makeup.filename2 = file2.name
        #     makeup.filename1 = file1.name
        #     makeup.save()
        #     return makeup
        if instance:
            instance.file = file
            instance.filename = file.name.split('/')[-1]
            instance.note = note
            instance.save()
            return instance
        return MakeUp.objects.create(
            order=order,
            file=file,
            filename=file.name,
            note=note,
        )


class MakeUpGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakeUp
        fields = '__all__'
