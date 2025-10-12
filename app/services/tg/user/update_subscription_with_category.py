from bot.filters.callback.category_callback import CategoryCallback
from enums.category_subscription_enum import CategorySubscriptionEnum
from models.category import Category
from models.user import User
from repositories.categories.get_category_by_id import get_category_by_id
from sqlalchemy.ext.asyncio import AsyncSession


async def update_subscription_with_category(
    category_callback: CategoryCallback,
    db: AsyncSession,
    subscribed_categories: list[Category],
    user: User,
) -> dict[str, str]:
    """
    Обновляет подписку пользователя на категорию.

    Args:
        category_callback (CategoryCallback): Callback-данные с идентификатором категории
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных
        subscribed_categories (list[Category]): Список категорий, на которые подписан пользователь
        user (User): Объект пользователя

    Returns:
        dict (str, str): Словарь с ключом "path_to_templates" и значением —
                         строкой, указывающей на шаблон ("subscribe" или "unsubscribe")

    Raises:
        ValueError: Если категория с указанным id не найдена
    """
    if not (category := await get_category_by_id(db, category_callback.category_id)):
        raise ValueError("Такой категории не найдено")

    template: str | None = None

    if category in subscribed_categories:
        user.categories.remove(category)
        template: str = CategorySubscriptionEnum.UNSUBSCRIBE.value
    else:
        user.categories.append(category)
        template: str = CategorySubscriptionEnum.SUBSCRIBE.value

    await db.commit()

    return {"path_to_templates": template}
