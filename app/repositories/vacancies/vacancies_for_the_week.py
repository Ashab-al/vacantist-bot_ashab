from models.user import User
from models.vacancy import Vacancy
from models.category import Category
from models.blacklist import BlackList
from sqlalchemy.ext.asyncio import AsyncSession
from services.tg.category.find_subscribe import find_subscribe
from enums.vacancies_for_the_week_enum import VacanciesForTheWeekStatusEnum
from sqlalchemy import func, select, Select
from datetime import datetime, timedelta, time


QUANTITY_DAYS = 7


class VacancyForTheWeekRepository:
    def __init__(
        self, 
        db: AsyncSession,
        subscribed_categories: list[Category] | list,
        user: User,
        page: int,
        page_size: int
    ):
        """
        Args:
            db (AsyncSession): Асинхронная сессия
            subscribed_categories (list[Category] | list): Список объектов `Category` на которые подписан пользователь
            stmt (Select): Исходный запрос (Select).
            page (int): Номер страницы (начиная с 1).
            page_size (int): Количество элементов на странице.
        
        """
        self.db: AsyncSession = db
        self.subscribed_categories: list[Category] | list = subscribed_categories
        self.user: User = user
        self.page: int = page
        self.page_size: int = page_size

    async def build_vacancies_for_the_week(
        self
    ) -> list[Vacancy] | list:
        """
        Вернуть список вакансий с примененной пагинацией

        Notes:
            self.vacancies_stmt: Сохраняет в экземпляре `VacancyForTheWeekRepository` базовый запрос, 
                                 чтобы потом получить общее количество найденных объектов
        """

        self.vacancies_stmt: Select = await self._base_stmt()

        stmt: Select = await self._apply_pagination(
            self.vacancies_stmt
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def total_count(
        self 
    ) -> int:
        """
        Считает записи, вошедшие в запрос.
        
        Returns:
            Общее количество записей.
        """

        count_stmt = self.vacancies_stmt.with_only_columns(func.count()).order_by(None)
        result = await self.db.execute(count_stmt)
        return result.scalar_one()

    async def _base_stmt(self) -> Select:
        """
        Вернуть базовый Select запрос для поиска вакансий по категориям
        """
        
        category_ids: set[int] = {
            category.id 
            for category in self.subscribed_categories
        }
        now_datetime: datetime = datetime.now()
        low_datetime: datetime = datetime.combine(
            now_datetime - timedelta(days=QUANTITY_DAYS), 
            time(hour=0, minute=0, second=0), 
            tzinfo=None
        )

        stmt: Select = (
            select(Vacancy)
            .where(
                Vacancy.category_id.in_(category_ids)
            )
            .where(Vacancy.platform_id.not_in(
                    select(BlackList.contact_information)    
                )
            )
            .where(
                Vacancy.created_at.between(low_datetime, now_datetime)
            )
            .order_by(Vacancy.created_at.desc())
        )
        
        return stmt
    
    async def _apply_pagination(
        self,
        stmt: Select    
    ) -> Select:
        """
        Применяет пагинацию к запросу.

        Args:
            stmt (Select): Запрос-Select
        
        Returns:
            Запрос с установленными limit и offset.
        
        """
        offset = (self.page - 1) * self.page_size
        return stmt.limit(self.page_size).offset(offset)