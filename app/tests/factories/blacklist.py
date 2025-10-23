import factory
from models.blacklist import BlackList


class BlacklistFactory(factory.Factory):
    """Фабрика для создания объектов модели `Category`."""

    class Meta:
        """Метаданные фабрики."""

        model = BlackList

    id: int = factory.Sequence(lambda n: n + 1)
    contact_information: str = factory.Faker("word")
    complaint_counter: str = 0
