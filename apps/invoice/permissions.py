from Bloom.permission import RoleBasedPermission


class InvoicePermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'invoice_reader'.
    - Other methods: Allowed only for 'admin'.
    """
    allowed_roles_get = {'admin', 'invoice_reader'}
    allowed_roles_post = {'admin', 'invoice'}
    allowed_roles_update = {'admin', 'invoice'}
    allowed_roles_delete = {'admin', 'invoice'}
