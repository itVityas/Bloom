from Bloom.permission import RoleBasedPermission


class StrihPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'strih_reader'.
    - Other methods: Allowed only for 'admin' and 'sgp'.
    """
    allowed_roles_get = {'admin', 'strih_reader'}
    allowed_roles_other = {'admin', 'strih'}
