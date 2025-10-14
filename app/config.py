"""
Конфигурация приложения и инициализация глобальных объектов.

- Настройки приложения через Pydantic Settings
- Настройка Jinja2 Environment для шаблонов
- Загрузка локализации i18n
- Глобальная очередь для вакансий
"""

import asyncio
import json
import logging
import os
from typing import Optional

import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
from lib.tg.pluralize import pluralize
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    """
    Настройки приложения, загружаются из .env файла.

    Attributes:
        bot_token (str): Токен Telegram бота
        admin_id (int): ID администратора
        admin_chat_id (str): ID чата администратора
        ngrok_api (str): URL локального ngrok API для получения публичного HTTPS URL
        database_dsn (str): DSN для подключения к базе данных
        echo_db_engine (Optional[bool]): Флаг логирования SQLAlchemy
        db_host (str), db_port (int), db_user (str), db_pass (str), db_name (str): параметры БД
        ngrok_authtoken (Optional[str]): токен для ngrok (если нужен)
    """

    bot_token: str
    admin_id: int
    admin_chat_id: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )
    ngrok_api: str

    # БД
    database_dsn: str
    echo_db_engine: Optional[bool] = True
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    ngrok_authtoken: Optional[str] = None

    #для продакшена
    domain_name: str
    subdomain: str
    pgadmin_subdomain: str
    directus_subdomain: str
    ssl_email: str
    postgres_password: str
    password_pgadmin: str
    secret: str
    mode: str

    def ngrok_url(self):
        """
        Получает публичный HTTPS URL от локального ngrok API.

        Returns:
            str: Публичный URL для вебхука
        """
        logging.info("Поиск Ngrok URL")
        response = requests.get(self.ngrok_api, timeout=10)
        response.raise_for_status()

        for tunnel in response.json().get("tunnels", []):
            if tunnel.get("proto") == "https":
                public_url = tunnel.get("public_url")
                logging.info("✅ Ngrok URL найден: %s", public_url)
                return public_url
        return None

    def get_webhook_url(self) -> str:
        """
        Формирует URL вебхука для Telegram бота.

        Returns:
            str: URL вебхука
        """
        if self.mode == "production":
            return f"https://{self.subdomain}.{self.domain_name}/api/v1/webhook"

        if self.mode == "develop":
            return f"{self.ngrok_url()}/api/v1/webhook"

        return None



settings = Settings()
"""Экземпляр настроек"""

jinja_env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    autoescape=select_autoescape(),
    enable_async=True,
)
"""Инициализация Jinja2 Environment для рендеринга шаблонов"""

# Загрузка локализации
with open(f"{BASE_DIR}/locales/ru-RU/bot.json", encoding="utf-8") as f:
    i18n: dict[str, str] = json.load(f)["ru"]
    """JSON с текстами для бота"""

jinja_env.globals["i18n"] = i18n
jinja_env.globals["pluralize"] = pluralize

vacancy_queue: asyncio.Queue = asyncio.Queue(maxsize=0)
"""Глобальная очередь вакансий"""
