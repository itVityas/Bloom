import django_filters as filters

from apps.account.models import User


class UserFilter(filters.FilterSet):
    """
    Filter class for filtering fields
    """
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    username = filters.CharFilter(field_name='username', lookup_expr='iexact')
    cont_username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    start_username = filters.CharFilter(field_name='username', lookup_expr='istartswith')
    end_username = filters.CharFilter(field_name='username', lookup_expr='iendswith')
    fio = filters.CharFilter(field_name='fio', lookup_expr='iexact')
    cont_fio = filters.CharFilter(field_name='fio', lookup_expr='icontains')
    start_fio = filters.CharFilter(field_name='fio', lookup_expr='istartswith')
    end_fio = filters.CharFilter(field_name='fio', lookup_expr='iendswith')
    departmant = filters.CharFilter(field_name='departmant', lookup_expr='iexact')
    cont_departmant = filters.CharFilter(field_name='departmant', lookup_expr='icontains')
    start_departmant = filters.CharFilter(field_name='departmant', lookup_expr='istartswith')
    end_departmant = filters.CharFilter(field_name='departmant', lookup_expr='iendswith')
    position = filters.CharFilter(field_name='position', lookup_expr='iexact')
    cont_position = filters.CharFilter(field_name='position', lookup_expr='icontains')
    start_position = filters.CharFilter(field_name='position', lookup_expr='istartswith')
    end_position = filters.CharFilter(field_name='position', lookup_expr='iendswith')
    room = filters.CharFilter(field_name='room', lookup_expr='iexact')
    cont_room = filters.CharFilter(field_name='room', lookup_expr='icontains')
    start_room = filters.CharFilter(field_name='room', lookup_expr='istartswith')
    end_room = filters.CharFilter(field_name='room', lookup_expr='iendswith')
    is_active = filters.BooleanFilter(field_name='is_active', lookup_expr='exact')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'cont_username',
            'start_username',
            'end_username',
            'fio',
            'cont_fio',
            'start_fio',
            'end_fio',
            'departmant',
            'cont_departmant',
            'start_departmant',
            'end_departmant',
            'position',
            'cont_position',
            'start_position',
            'end_position',
            'room',
            'cont_room',
            'start_room',
            'end_room',
            'is_active',
        ]
