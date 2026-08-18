"""File to get the settings."""

import configparser
from os import environ
from pathlib import Path

from contracts.enums.settings_enum import ConfigEnum
from contracts.protocols.config_protocol import ConfigServiceProtocol


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE_PATH = PROJECT_ROOT / ".env"
LEGACY_CONFIG_PATH = PROJECT_ROOT / "config.ini"


def _load_dotenv_file() -> None:
    if not ENV_FILE_PATH.exists():
        return

    for raw_line in ENV_FILE_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = [part.strip() for part in line.split("=", 1)]
        if not key:
            continue

        value = value.strip().strip("\"'")
        environ.setdefault(key, value)


_load_dotenv_file()


@DeprecationWarning
def read_azure_service_bus_config():
    return {
        "connection_string": EnvironConfig().get_config_value(
            ConfigEnum.AZURE_SERVICE_BUS_CONNECTION_STRING
        ),
        "queue_name": EnvironConfig().get_config_value(
            ConfigEnum.AZURE_SERVICE_BUS_QUEUE_NAME
        ),
    }


@DeprecationWarning
def read_telegram_bot_config():
    return {
        "bot_token": EnvironConfig().get_config_value(ConfigEnum.TELEGRAM_BOT_TOKEN)
    }


class ConfigParserService(ConfigServiceProtocol):
    def __init__(self):
        super().__init__()
        self.file_path = str(ENV_FILE_PATH)

    def get_config_value(self, service_name: ConfigEnum) -> str:
        _load_dotenv_file()
        value = EnvironConfig().get_config_value(service_name)
        if value is not None:
            return value

        legacy_config = configparser.ConfigParser()
        if LEGACY_CONFIG_PATH.exists():
            legacy_config.read(LEGACY_CONFIG_PATH)
            section, key = service_name.value
            if legacy_config.has_option(section, key):
                return legacy_config.get(section, key)

        return ConfigEnum.get_default(service_name)


class EnvironConfig(ConfigServiceProtocol):
    def __init__(self):
        _load_dotenv_file()

    def get_config_value(self, service_name: ConfigEnum) -> str:
        section, key = service_name.value
        normalized_section = section.upper().replace("-", "_").replace(" ", "_")
        normalized_key = key.upper().replace("-", "_").replace(" ", "_")

        candidates = [
            f"{normalized_section}_{normalized_key}",
            f"{normalized_section}{normalized_key}",
            normalized_key,
            f"{section.upper()}_{key.upper()}",
            f"{section.upper()}{key.upper()}",
        ]

        for candidate in candidates:
            value = environ.get(candidate)
            if value is not None:
                return value

        return ConfigEnum.get_default(service_name)
