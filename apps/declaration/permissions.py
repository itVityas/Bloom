from Bloom.permission import RoleBasedPermission


class DeclarationPermission(RoleBasedPermission):
    """
    Permission for declaration operations.
    - GET: Allowed for 'admin', 'arrival_reader' and 'declaration_writer'.
    - Other methods: Allowed for 'admin' and 'declaration_writer'.
    """
    allowed_roles_get = {'admin', 'arrival_reader', 'declaration_writer'}
    allowed_roles_post = {'admin', 'declaration_writer'}
    allowed_roles_update = {'admin', 'declaration_writer', 'decl_update', 'declaration_block_unblock'}
    allowed_roles_delete = {'admin', 'declaration_delete'}
