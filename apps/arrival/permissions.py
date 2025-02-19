from rest_framework.permissions import BasePermission


class ArrivalPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_roles = [user_role.role.name for user_role in user.userroles_set.all()]

        if request.method == 'GET':
            allowed_roles = {'admin', 'arrival_reader'}
        else:
            allowed_roles = {'admin'}

        if allowed_roles.intersection(user_roles):
            return True
        return False


class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_roles = [user_role.role.name for user_role in user.userroles_set.all()]

        if request.method == 'GET':
            allowed_roles = {'admin', 'arrival_reader', 'order_writer'}
        else:
            allowed_roles = {'admin',  'order_writer'}

        if allowed_roles.intersection(user_roles):
            return True

        return False


class ContainerPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_roles = [user_role.role.name for user_role in user.userroles_set.all()]

        if request.method == 'GET':
            allowed_roles = {'admin', 'arrival_reader', 'container_writer'}
        else:
            allowed_roles = {'admin',  'container_writer'}

        if allowed_roles.intersection(user_roles):
            return True

        return False


class DeclarationPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_roles = [user_role.role.name for user_role in user.userroles_set.all()]

        if request.method == 'GET':
            allowed_roles = {'admin', 'arrival_reader', 'declaration_writer'}
        else:
            allowed_roles = {'admin', 'declaration_writer'}

        if allowed_roles.intersection(user_roles):
            return True

        return False


class ContentPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_roles = [user_role.role.name for user_role in user.userroles_set.all()]

        if request.method == 'GET':
            allowed_roles = {'admin', 'arrival_reader', 'content_writer'}
        else:
            allowed_roles = {'admin', 'content_writer'}

        if allowed_roles.intersection(user_roles):
            return True

        return False