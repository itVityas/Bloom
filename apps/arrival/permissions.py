from rest_framework.permissions import BasePermission


class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_roles = [userrole.role.name for userrole in user.userroles_set.all()]

        if request.method == 'GET':
            allowed_roles = {'admin', 'arrival_writer', 'arrival_reader'}
        else:
            allowed_roles = {'admin', 'arrival_writer'}

        if allowed_roles.intersection(user_roles):
            return True
        return False
