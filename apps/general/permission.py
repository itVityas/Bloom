from Bloom.permission import RoleBasedPermission


class AddPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'add'.
    - Other methods: Allowed only for 'admin' and 'sgp'.
    """
    allowed_roles_get = None
    allowed_roles_post = {'admin', 'add'}
    allowed_roles_update = {'admin', 'add'}
    allowed_roles_delete = {'admin', 'add'}
