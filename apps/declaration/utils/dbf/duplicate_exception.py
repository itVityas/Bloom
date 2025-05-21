class DuplicateDeclarationException(Exception):
    def __init__(self, duplicate_ids):
        self.duplicate_ids = duplicate_ids
        super().__init__(f"Декларации с declaration_ids {duplicate_ids} уже существуют.")
