from rest_framework import serializers

from apps.general.models import Visits


class VisitsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Visits
        fields = '__all__'

    def validate(self, attrs):
        user = attrs.get('user', None)
        if not user:
            raise serializers.ValidationError('user is required')
        visits = Visits.objects.filter(user=user).order_by('id')
        if visits.count() > 4:
            this_visit = Visits.objects.filter(user=user, label=attrs.get('label'))
            if this_visit:
                this_visit.delete()
        return attrs
