from Bloom.permission import RoleBasedPermission


class ArrivalPermission(RoleBasedPermission):
    """
    Permission for arrival operations.
    - GET: Allowed for 'admin' and 'arrival_reader'.
    - Other methods: Allowed only for 'admin'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'order_writer', 'container_writer'}
    allowed_roles_post = {'admin', 'order_writer', 'container_writer'}
    allowed_roles_update = {'admin', 'order_writer', 'container_writer'}
    allowed_roles_delete = {'admin', 'order_writer', 'container_writer'}


class OrderPermission(RoleBasedPermission):
    """
    Permission for order operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'order_writer'.
    - Other methods: Allowed for 'admin' and 'order_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'order_writer', 'container_writer'}
    allowed_roles_post = {'admin', 'order_writer', 'container_writer'}
    allowed_roles_update = {'admin', 'order_writer', 'container_writer'}
    allowed_roles_delete = {'admin', 'order_writer', 'container_writer'}


class ContainerPermission(RoleBasedPermission):
    """
    Permission for container operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'container_writer'.
    - Other methods: Allowed for 'admin' and 'container_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'container_writer'}
    allowed_roles_post = {'admin', 'container_writer'}
    allowed_roles_update = {'admin', 'container_writer'}
    allowed_roles_delete = {'admin', 'container_writer'}


class ContentPermission(RoleBasedPermission):
    """
    Permission for content operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'content_writer'.
    - Other methods: Allowed for 'admin' and 'content_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'container_writer'}
    allowed_roles_post = {'admin', 'container_writer'}
    allowed_roles_update = {'admin', 'container_writer'}
    allowed_roles_delete = {'admin', 'container_writer'}
