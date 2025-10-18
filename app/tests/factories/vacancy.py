import factory
from lib.tg.constants import SOURCE
from models.vacancy import Vacancy


class VacancyWithCategoryFactory(factory.Factory):
    """Фабрика для создания объектов модели `Vacancy` с категорией."""

    class Meta:
        """Метаданные фабрики."""

        model = Vacancy

    id: int = factory.Sequence(lambda n: n + 1)
    title: str = factory.Faker("sentence", nb_words=6)
    description: str = factory.Faker("sentence", nb_words=30)
    contact_information: str = factory.Faker("email")
    source: str = SOURCE
    platform_id: str = factory.Sequence(lambda n: f"{n + 1}")
    category = factory.SubFactory("tests.factories.category.CategoryFactory")


class VacancyWithoutCategoryFactory(factory.Factory):
    """Фабрика для создания объектов модели `Vacancy` без категории."""

    class Meta:
        """Метаданные фабрики."""

        model = Vacancy

    id: int = factory.Sequence(lambda n: n + 1)
    title: str = factory.Faker("sentence", nb_words=6)
    description: str = factory.Faker("sentence", nb_words=30)
    contact_information: str = factory.Faker("email")
    source: str = SOURCE
    platform_id: str = factory.Sequence(lambda n: f"{n + 1}")
    category = None
