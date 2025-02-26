from rest_framework.permissions import BasePermission


class RoleBasedPermission(BasePermission):
    """
    Base permission class for role-based access.
    Child classes should define the allowed roles for GET requests (allowed_roles_get)
    and for non-GET requests (allowed_roles_other).
    """
    allowed_roles_get = set()
    allowed_roles_other = set()

    def has_permission(self, request, view):
        user = request.user
        # Get set of role names assigned to the user.
        user_roles = {user_role.role.name for user_role in user.userroles_set.all()}

        if request.method == 'GET':
            allowed_roles = self.allowed_roles_get
        else:
            allowed_roles = self.allowed_roles_other

        # Return True if there is any intersection between user roles and allowed roles.
        return bool(user_roles.intersection(allowed_roles))


class ArrivalPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'arrival_reader'.
    - Other methods: Allowed only for 'admin'.
    """
    allowed_roles_get = {'admin', 'arrival_reader'}
    allowed_roles_other = {'admin'}


class OrderPermission(RoleBasedPermission):
    """
    Permission for order operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'order_writer'.
    - Other methods: Allowed for 'admin' and 'order_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'order_writer'}
    allowed_roles_other = {'admin', 'order_writer'}


class ContainerPermission(RoleBasedPermission):
    """
    Permission for container operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'container_writer'.
    - Other methods: Allowed for 'admin' and 'container_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'container_writer'}
    allowed_roles_other = {'admin', 'container_writer'}


class DeclarationPermission(RoleBasedPermission):
    """
    Permission for declaration operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'declaration_writer'.
    - Other methods: Allowed for 'admin' and 'declaration_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'declaration_writer'}
    allowed_roles_other = {'admin', 'declaration_writer'}


class ContentPermission(RoleBasedPermission):
    """
    Permission for content operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'content_writer'.
    - Other methods: Allowed for 'admin' and 'content_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'content_writer'}
    allowed_roles_other = {'admin', 'content_writer'}


class ClearanceInvoicePermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoice operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'clearance_invoice_writer'.
    - Other methods: Allowed for 'admin' and 'clearance_invoice_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'clearance_invoice_writer'}
    allowed_roles_other = {'admin', 'content_writer'}


class ClearanceInvoiceItemsPermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoiceItems operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'clearance_invoice_items_writer'.
    - Other methods: Allowed for 'admin' and 'clearance_invoice_items_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'clearance_invoice_items_writer'}
    allowed_roles_other = {'admin', 'clearance_invoice_items_writer'}


class ClearedItemPermission(RoleBasedPermission):
    """
    Permission for ClearanceInvoice operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'cleared_item_writer'.
    - Other methods: Allowed for 'admin' and 'cleared_item_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'cleared_item_writer'}
    allowed_roles_other = {'admin', 'cleared_item_writer'}
