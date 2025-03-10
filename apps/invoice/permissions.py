from Bloom.permission import RoleBasedPermission


class InvoicePermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'invoice_reader'.
    - Other methods: Allowed only for 'admin'.
    """
    allowed_roles_get = {'admin', 'invoice_reader'}
    allowed_roles_other = {'admin', 'invoice'}
