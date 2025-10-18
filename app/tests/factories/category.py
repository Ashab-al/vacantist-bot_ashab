import factory
from models.category import Category


class CategoryFactory(factory.Factory):
    """Фабрика для создания объектов модели `Category`."""

    class Meta:
        """Метаданные фабрики."""

        model = Category

    id: int = factory.Sequence(lambda n: n + 1)
    name: str = factory.Faker("word")
