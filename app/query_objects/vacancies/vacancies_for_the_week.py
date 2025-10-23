from datetime import datetime, time, timedelta

from models.blacklist import BlackList
from models.category import Category
from models.user import User
from models.vacancy import Vacancy
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

QUANTITY_DAYS = 7


class VacancyForTheWeekQuery:
    """
    Репозиторий для получения вакансий за последнюю неделю
    для пользователя с учетом его подписок на категории.
    """

    def __init__(
        self,
        db: AsyncSession,
        user: User,
        page: int,
        page_size: int,
    ):
        """
        Args:
            db (AsyncSession): Асинхронная сессия
            subscribed_categories (list[Category] | list): Список объектов `Category`
                на которые подписан пользователь
            user (User): Пользователь, для которого ищем вакансии.
            stmt (Select): Исходный запрос (Select).
            page (int): Номер страницы (начиная с 1).
            page_size (int): Количество элементов на странице.
        """

        self.db: AsyncSession = db
        self.user: User = user
        self.page: int = page
        self.page_size: int = page_size
        self.vacancies_stmt: Select | None = None

    async def build_vacancies_for_the_week(
        self, subscribed_categories: list[Category]
    ) -> list[Vacancy] | list:
        """
        Получить список вакансий за последнюю неделю с учетом пагинации.

        Notes:
            self.vacancies_stmt: сохраняет базовый запрос для последующего
                подсчета общего количества записей.

        Returns:
            list[Vacancy]: Список вакансий для текущей страницы.
        """

        self.vacancies_stmt: Select = await self._base_stmt(subscribed_categories)
        stmt: Select = await self._apply_pagination(self.vacancies_stmt)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def total_count(self) -> int:
        """
        Посчитать общее количество вакансий, подходящих под условия поиска.

        Returns:
            int: Общее количество найденных вакансий.
        """

        count_stmt = self.vacancies_stmt.with_only_columns(func.count()).order_by(
            None
        )  # pylint: disable=not-callable
        result = await self.db.execute(count_stmt)
        return result.scalar_one()

    async def _base_stmt(self, subscribed_categories: list[Category]) -> Select:
        """
        Построить базовый Select-запрос для вакансий пользователя.

        Returns:
            Select: SQLAlchemy Select-запрос с фильтрацией по категориям,
                    blacklist и дате создания.
        """
        category_ids: set[int] = {category.id for category in subscribed_categories}
        now_datetime: datetime = datetime.now()
        low_datetime: datetime = datetime.combine(
            now_datetime - timedelta(days=QUANTITY_DAYS),
            time(hour=0, minute=0, second=0),
            tzinfo=None,
        )

        stmt: Select = (
            select(Vacancy)
            .where(Vacancy.category_id.in_(category_ids))
            .where(Vacancy.platform_id.not_in(select(BlackList.contact_information)))
            .where(Vacancy.created_at.between(low_datetime, now_datetime))
            .order_by(Vacancy.created_at.desc())
        )

        return stmt

    async def _apply_pagination(self, stmt: Select) -> Select:
        """
        Применить пагинацию к запросу.

        Args:
            stmt (Select): Исходный Select-запрос.

        Returns:
            Select: Запрос с установленными `limit` и `offset`.
        """

        offset = (self.page - 1) * self.page_size
        return stmt.limit(self.page_size).offset(offset)
