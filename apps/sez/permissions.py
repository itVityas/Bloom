from Bloom.permission import RoleBasedPermission


class STZPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'stz_reader'.
    - Other methods: Allowed only for 'admin'.
    """
    allowed_roles_get = {'admin', 'stz_reader'}
    allowed_roles_other = {'admin'}
