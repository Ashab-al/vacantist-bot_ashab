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
from enums.mode_enum import ModeEnum
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
        url_for_local_develop (str): URL для локальной разработки
        database_dsn (str): DSN для подключения к базе данных
        echo_db_engine (Optional[bool]): Флаг логирования SQLAlchemy
        db_host (str), db_port (int), db_user (str), db_pass (str), db_name (str): параметры БД
    """

    bot_token: str
    admin_id: int
    admin_chat_id: str
    url_for_local_develop: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        extra="ignore",
    )

    mailing_vacancies_thread_id: int
    mailing_payments_thread_id: int
    mailing_errors_thread_id: int
    mailing_new_users_thread_id: int
    mailing_new_spam_vacancies_thread_id: int
    # БД
    database_dsn: str
    echo_db_engine: Optional[bool] = True
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    # proxy
    proxy_host: str
    proxy_port: int
    proxy_user: str
    proxy_pass: str

    # Задержки для рассылки вакансий
    min_delay_seconds: int
    max_delay_seconds: int

    # для продакшена
    domain_name: str
    subdomain: str
    directus_subdomain: str
    n8n_subdomain: str
    directus_db_client: str
    ssl_email: str
    postgres_password: str
    password_directus: str
    secret: str
    mode: ModeEnum
    generic_timezone: str

    def get_webhook_url(self) -> str:
        """
        Формирует URL вебхука для Telegram бота.

        Returns:
            str: URL вебхука
        """
        if self.mode == ModeEnum.PRODUCTION:
            return f"https://{self.subdomain}.{self.domain_name}/api/v1/webhook"

        return f"{self.url_for_local_develop}/api/v1/webhook"


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
