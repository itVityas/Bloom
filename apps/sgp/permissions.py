from Bloom.permission import RoleBasedPermission


class SGPPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'sgp_reader'.
    - Other methods: Allowed only for 'admin' and 'sgp'.
    """
    allowed_roles_get = {'admin', 'sgp_reader'}
    allowed_roles_other = {'admin', 'sgp'}
