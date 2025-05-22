from Bloom.permission import RoleBasedPermission


class SGPPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'sgp_reader'.
    - Other methods: Allowed only for 'admin' and 'sgp'.
    """
    allowed_roles_get = {'admin', 'sgp_reader', 'sgp', 'ban'}
    allowed_roles_post = {'admin', 'sgp', 'ban'}
    allowed_roles_update = {'admin', 'sgp', 'ban'}
    allowed_roles_delete = {'admin', 'sgp', 'ban'}
