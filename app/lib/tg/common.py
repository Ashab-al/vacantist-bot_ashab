from config import jinja_env


async def jinja_render(action, hash={}) -> str:
    """
    Асинхронно рендерит HTML-шаблон Jinja.

    Args:
        action (str): Название действия, соответствующее имени шаблона.
        hash (dict, optional): Словарь с переменными для подстановки в шаблон. По умолчанию пустой.

    Returns:
        str: Отрендеренный HTML-код.
    """
    return await jinja_env.get_template(f"/bot/{action}.jinja").render_async(**hash)
