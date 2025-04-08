class DuplicateDeclarationException(Exception):
    def __init__(self, duplicate_ids):
        self.duplicate_ids = duplicate_ids
        super().__init__(f"Declarations with declaration_ids {duplicate_ids} already exist.")
