import os

import typer
from pydantic import BaseSettings

from src.logger import configure_log_handlers, get_logger


class DevelopmentConfig(BaseSettings):
    app_name: str = "python-app-starter"
    environment: str = "dev"

    # logging
    log_console: bool = True
    log_file: str = "main.log"

    message: str = "default message"

    class Config:
        env_file = ".env"


class StagingConfig(DevelopmentConfig):
    environment = "stg"
    log_file = ""


class ProductionConfig(DevelopmentConfig):
    environment = "prod"
    log_file = ""


def get_config(environment: str = os.environ.get("ENVIRONMENT", "dev")) -> DevelopmentConfig:
    configs = {
        "dev": DevelopmentConfig(),
        "stg": StagingConfig(),
        "prod": ProductionConfig(),
    }
    return configs[environment]


config = get_config()

# config logger
configure_log_handlers(config.log_console, config.log_file)
logger = get_logger(config.app_name)
logger.debug("config", extra={"config": config.dict()})


def main(key: str) -> None:
    """
    Print config value of specified key.
    """
    typer.echo(config.dict().get(key))


if __name__ == "__main__":
    typer.run(main)
