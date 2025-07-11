from Bloom.permission import RoleBasedPermission


class SGPPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'sgp_reader' and 'ban'.
    - Other methods: Allowed only for 'admin' and 'ban'.
    """
    allowed_roles_get = {'admin', 'warehouse', 'warehouse_writer'}
    allowed_roles_post = {'admin', 'warehouse_writer'}
    allowed_roles_update = {'admin', 'warehouse_writer'}
    allowed_roles_delete = {'admin', 'warehouse_writer'}
