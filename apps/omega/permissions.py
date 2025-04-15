from Bloom.permission import RoleBasedPermission


class OmegaPermission(RoleBasedPermission):
    """
    Permission for omega operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'omegan_writer'.
    - Other methods: Allowed for 'admin' and 'omega_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'omega_writer'}
    allowed_roles_other = {'admin', 'omega_writer'}
