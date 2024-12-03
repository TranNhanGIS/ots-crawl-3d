"""
config.py

- This module initializes and configures application settings using the Pydantic `BaseSettings` class.
- It supports environment-specific configurations via `.env` files
- Enhances debugging output with `rich`-styled tracebacks.
- Configure loguru logger to write log entries to a rotating log file.
"""

from pydantic_settings import BaseSettings
from rich.traceback import install as rich_installer
from loguru import logger
from datetime import datetime

rich_installer()
# pylint: disable=R0903

logger.add(
    f"logs/log_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log",
    rotation="1 week",
    retention="1 month",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)


class Settings(BaseSettings):
    """
    Manages application settings by loading configurations from environment variables.
    """

    debug: bool = False
    crawler_url: str = ""
    blender_exe: str = ""

    class Config:
        """
        Configuration for loading environment variables from the .env file.
        """

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
