from rest_framework.exceptions import ValidationError


class DuplicateContainerException(ValidationError):
    value = 'Контейнер с таким именем уже существует'

    def __init__(self, container_name):
        self.value = f"Контейнер {container_name} уже существует"
        super().__init__(self.value)

    def __str__(self):
        return self.value
