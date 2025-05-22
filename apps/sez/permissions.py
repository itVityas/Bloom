from Bloom.permission import RoleBasedPermission


class STZPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'stz_reader'.
    - Other methods: Allowed only for 'admin'.
    """
    allowed_roles_get = {'admin', 'stz_reader', 'stz'}
    allowed_roles_post = {'admin', 'stz'}
    allowed_roles_update = {'admin', 'stz'}
    allowed_roles_delete = {'admin', 'stz'}


class ClearanceInvoicePermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoice operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'clearance_invoice_writer'.
    - Other methods: Allowed for 'admin' and 'clearance_invoice_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'stz_reader', 'stz', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer', 'stz'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer', 'stz'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer', 'stz'}


class ClearanceInvoiceItemsPermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoiceItems operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'clearance_invoice_items_writer'.
    - Other methods: Allowed for 'admin' and 'clearance_invoice_items_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'stz_reader', 'stz', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer', 'stz'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer', 'stz'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer', 'stz'}


class ClearedItemPermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoice operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'cleared_item_writer'.
    - Other methods: Allowed for 'admin' and 'cleared_item_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'stz_reader', 'stz', 'clearance_invoice_writer'}
    allowed_roles_post = {'admin', 'clearance_invoice_writer', 'stz'}
    allowed_roles_update = {'admin', 'clearance_invoice_writer', 'stz'}
    allowed_roles_delete = {'admin', 'clearance_invoice_writer', 'stz'}


class InnerTTNPermission(RoleBasedPermission):
    """
    Permission for InnerTTn operations.
    - GET: Allowed for 'admin', 'stz' and 'stz_reader', 'ttn'.
    - Other methods: Allowed for 'admin' and 'stz', 'ttn'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'stz', 'stz_reader', 'ttn'}
    allowed_roles_post = {'admin', 'stz', 'ttn'}
    allowed_roles_update = {'admin', 'stz', 'ttn'}
    allowed_roles_delete = {'admin', 'stz', 'ttn'}
