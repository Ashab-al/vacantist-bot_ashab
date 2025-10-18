import factory
from enums.bot_status_enum import BotStatusEnum
from factory.alchemy import SQLAlchemyModelFactory
from models.user import User


class UserFactoryWithoutSubscriptions(factory.Factory):
    """
    Фабрика для создания объектов модели `User` без связанных подписок.

    Используется для тестирования сценариев, где не требуется наличие подписок у пользователя.
    Атрибуты генерируются автоматически:
    - `id`: Уникальный идентификатор, увеличивается на 1 для каждого нового экземпляра.
    - `platform_id`: Уникальный идентификатор платформы, увеличивается на 1.
    - `categories`: Пустой список (отсутствие подписок).
    - `first_name`: Случайное имя, сгенерированное с помощью библиотеки `Faker`.
    """

    class Meta:
        """Метаданные фабрики."""

        model = User

    id: int = factory.Sequence(lambda n: n + 1)
    platform_id: int = factory.Sequence(lambda n: n + 1)
    categories: list = factory.LazyAttribute(lambda _: [])
    first_name: str = factory.Faker("name")
    point: int = 0
    bonus: int = 0
    bot_status: BotStatusEnum = BotStatusEnum.WORKS
