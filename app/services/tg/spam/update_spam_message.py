from aiogram.types import CallbackQuery
from lib.tg.common import jinja_render


async def update_spam_message(
    callback: CallbackQuery,
    action: str,
    context: dict | None = None,
) -> None:
    """
    Обновляет текст сообщения в админ-группе с использованием шаблона Jinja2.

    Подставляет данные в указанный шаблон и редактирует исходное сообщение.
    В контекст шаблона автоматически передаётся текущий текст сообщения (`callback.message.text`),
    а также дополнительные переменные из `context`.

    :param callback: Объект CallbackQuery, содержащий ссылку на сообщение, которое нужно обновить.
    :param action: Название шаблона Jinja2 (например, 'spam/increment_user_bonus'),
                   используемого для генерации нового текста.
    :param context: Дополнительные данные для шаблона. Опционально.
                    Если не передан, используется пустой словарь.
    :return: None
    """
    await callback.message.edit_text(
        text=await jinja_render(
            action, {"text": callback.message.text, **(context or {})}
        ),
        reply_markup=callback.message.reply_markup,
    )
