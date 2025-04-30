from rest_framework.permissions import BasePermission


class RoleBasedPermission(BasePermission):
    """
    Base permission class for role-based access.
    Child classes should define the allowed roles for GET requests (allowed_roles_get)
    and for non-GET requests (allowed_roles_other).
    """
    allowed_roles_get = set()
    allowed_roles_post = set()
    allowed_roles_update = set()
    allowed_roles_delete = set()

    def has_permission(self, request, view):
        user = request.user
        # Get set of role names assigned to the user.
        user_roles = {user_role.role.name for user_role in user.userroles_set.all()}

        if request.method == 'GET':
            allowed_roles = self.allowed_roles_get
        elif request.method == 'POST':
            allowed_roles = self.allowed_roles_post
        elif request.method == 'PUT' or request.method == 'PATCH':
            allowed_roles = self.allowed_roles_update
        else:
            allowed_roles = self.allowed_roles_delete

        # Return True if there is any intersection between user roles and allowed roles.
        return bool(user_roles.intersection(allowed_roles))
