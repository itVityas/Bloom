from Bloom.permission import RoleBasedPermission


class StrihPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'strih_reader'.
    - Other methods: Allowed only for 'admin' and 'sgp'.
    """
    allowed_roles_get = None
    allowed_roles_post = {'admin', 'strih'}
    allowed_roles_update = {'admin', 'strih'}
    allowed_roles_delete = {'admin', 'strih'}
