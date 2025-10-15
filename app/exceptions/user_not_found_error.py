class UserNotFoundError(Exception):
    """Пользователь не найден в базе."""

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"пользователь с ID {user_id} не найден")
