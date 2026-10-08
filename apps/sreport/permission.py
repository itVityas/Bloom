from Bloom.permission import RoleBasedPermission


class ProductPlanPermission(RoleBasedPermission):
    """
    Permission for Strih operations.
    - GET: Allowed for all.
    - Other methods: Allowed only for 'admin' and 'strih'.
    """
    allowed_roles_get = None
    allowed_roles_post = {'admin', 'factoryAdministation'}
    allowed_roles_update = {'admin', 'factoryAdministation'}
    allowed_roles_delete = {'admin', 'factoryAdministation'}
