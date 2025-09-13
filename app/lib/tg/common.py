from config import jinja_env

async def jinja_render(
    action, 
    hash = {}
) -> str:
    """Вернуть отрендеренный html """
    return await (jinja_env.get_template(f"/bot/{action}.jinja")).render_async(**hash)