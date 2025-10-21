class CategoryAlreadyExistError(Exception):
    """Категория уже существует в базе."""

    def __init__(self):
        super().__init__("Такая категория уже существует")
