from Bloom.permission import RoleBasedPermission


class OmegaPermission(RoleBasedPermission):
    """
    Permission for omega operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'omegan_writer'.
    - Other methods: Allowed for 'admin' and 'omega_writer'.
    """
    allowed_roles_get = None
    allowed_roles_post = {'admin', 'omega_writer'}
    allowed_roles_update = {'admin', 'omega_writer'}
    allowed_roles_delete = {'admin', 'omega_writer'}
