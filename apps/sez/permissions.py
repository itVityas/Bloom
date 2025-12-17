from Bloom.permission import RoleBasedPermission


class STZPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'stz_reader', 'clearance_invoice_writer'.
    - Other methods: Allowed only for 'admin' and 'clearance_invoice_writer'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer'}


class ClearanceInvoicePermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoice operations.
    - GET: Allowed for 'admin', 'stz_reader' and 'clearance_invoice_writer'.
    - Other methods: Allowed for 'admin' and 'clearance_invoice_writer'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer'}


class ClearanceInvoiceItemsPermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoiceItems operations.
    - GET: Allowed for 'admin', 'stz_reader' and 'clearance_invoice_writer'.
    - Other methods: Allowed for 'admin' and 'clearance_invoice_writer'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer'}


class ClearedItemPermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoice operations.
    - GET: Allowed for 'admin', 'stz_reader' and 'clearance_invoice_writer'.
    - Other methods: Allowed for 'admin' and 'clearance_invoice_writer'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer', 'add_cleared_items'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer', 'add_cleared_items'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer',
                            'delete_user_cleared_item', 'delete_rogram_cleared_items'}


class InnerTTNPermission(RoleBasedPermission):
    """
    Permission for InnerTTn operations.
    - GET: Allowed for 'admin', and 'stz_reader', 'ttn_writer'.
    - Other methods: Allowed for 'admin' and 'stz', 'ttn_writer'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'ttn_writer'}
    allowed_roles_post = {'admin', 'ttn_writer'}
    allowed_roles_update = {'admin', 'ttn_writer'}
    allowed_roles_delete = {'admin', 'ttn_writer'}
