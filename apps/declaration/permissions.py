from Bloom.permission import RoleBasedPermission


class DeclarationPermission(RoleBasedPermission):
    """
    Permission for declaration operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'declaration_writer'.
    - Other methods: Allowed for 'admin' and 'declaration_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'declaration_writer'}
    allowed_roles_other = {'admin', 'declaration_writer'}
