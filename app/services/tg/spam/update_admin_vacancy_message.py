

async def update_admin_vacancy_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    vacancy_id: int,
    session: AsyncSession
) -> None:
    """
    Обновляет сообщение о вакансии в админ-группе после того, как вакансия была признана спамом.

    Args:
        bot (Bot): Экземпляр Telegram бота для отправки сообщений.
        chat_id (int): ID чата, где находится сообщение о вакансии.
        message_id (int): ID сообщения, которое нужно обновить.
        vacancy_id (int): ID вакансии, которая была признана спамом.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.

    Returns:
        None
    """
    # Здесь должна быть логика получения информации о вакансии по vacancy_id,
    # формирование нового текста сообщения и его обновление через Telegram API.
    pass