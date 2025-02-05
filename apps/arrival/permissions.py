from rest_framework.permissions import BasePermission


class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        user_roles = list([userroles.role.name for userroles in user.userroles_set.all()])
        if request.method == 'GET':
            if set(('admin', 'arrival_writer', 'arrival_reader')).intersection(user_roles):
                return True
        else:
            if set(('admin', 'arrival_writer')).intersection(user_roles):
                return True
        return False
