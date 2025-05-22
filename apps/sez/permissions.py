from Bloom.permission import RoleBasedPermission


class STZPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'stz_reader'.
    - Other methods: Allowed only for 'admin'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer'}


class ClearanceInvoicePermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoice operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'clearance_invoice_writer'.
    - Other methods: Allowed for 'admin' and 'clearance_invoice_writer'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer'}


class ClearanceInvoiceItemsPermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoiceItems operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'clearance_invoice_items_writer'.
    - Other methods: Allowed for 'admin' and 'clearance_invoice_items_writer'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer'}


class ClearedItemPermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoice operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'cleared_item_writer'.
    - Other methods: Allowed for 'admin' and 'cleared_item_writer'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer'}


class InnerTTNPermission(RoleBasedPermission):
    """
    Permission for InnerTTn operations.
    - GET: Allowed for 'admin', 'stz' and 'stz_reader', 'ttn'.
    - Other methods: Allowed for 'admin' and 'stz', 'ttn'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'ttn_writer'}
    allowed_roles_post = {'admin', 'ttn_writer'}
    allowed_roles_update = {'admin', 'ttn_writer'}
    allowed_roles_delete = {'admin', 'ttn_writer'}
