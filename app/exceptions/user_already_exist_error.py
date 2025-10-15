class UserAlreadyExistError(Exception):
    """Пользователь уже существует в базе."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"Пользователь с ID {user_id} уже существует")