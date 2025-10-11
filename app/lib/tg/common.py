from config import jinja_env


async def jinja_render(action, context: dict | None = None) -> str:
    """
    Асинхронно рендерит HTML-шаблон Jinja.

    Args:
        action (str): Название действия, соответствующее имени шаблона.
        context (dict, optional): Словарь с переменными для подстановки в шаблон.
            По умолчанию пустой.

    Returns:
        str: Отрендеренный HTML-код.
    """
    if context is None:
        context = {}
    return await jinja_env.get_template(f"/bot/{action}.jinja").render_async(**context)
