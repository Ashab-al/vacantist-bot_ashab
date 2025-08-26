import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from typing import Optional
import logging
import requests


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_ID: int
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )
    ngrok_api: str

    database_dsn: str
    echo_db_engine: Optional[bool] = True
    db_host: str
    db_port: int
    db_user: str
    db_user: str
    db_pass: str
    db_name: str

    ngrok_authtoken: Optional[str] = None

    def ngrok_url(self):
        """Получает публичный HTTPS URL от локального API ngrok."""
        logging.info(f"Поиск Ngrok URL")
        response = requests.get(self.ngrok_api)
        response.raise_for_status()

        for tunnel in response.json().get("tunnels", []):
            if tunnel.get("proto") == "https":
                public_url = tunnel.get("public_url")
                logging.info(f"✅ Ngrok URL найден: {public_url}")
                return public_url

    def get_webhook_url(self) -> str:
        """Возвращает URL вебхука с кодированием специальных символов."""
        return f"{self.ngrok_url()}/api/v1/webhook"


settings = Settings()