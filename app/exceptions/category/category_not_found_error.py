class CategoryNotFoundError(Exception):
    """Категория не найден в базе."""

    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__(f"Категория с ID {self.category_id} не найдена")
