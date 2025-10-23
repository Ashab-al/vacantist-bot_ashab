class CategoryNotFoundError(Exception):
    """Категория не найден в базе."""

    def __init__(self, category_id: int | None = None):
        self.category_id = category_id
        super().__init__(
            f"Категория не найдена с ID {self.category_id}"
            if category_id
            else "Такой категории не существует"
        )
