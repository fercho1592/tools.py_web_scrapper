from enum import Enum
from typing import Self


class ConfigEnum(Enum):
    LOG_LEVEL = ("General", "log_level")
    E_MANGA_DOMAIN = ("MangaStrategy", "e_manga_domain")
    TMH_MANGA_DOMAIN = ("MangaStrategy", "tmh_manga_domain")
    AZURE_SERVICE_BUS_CONNECTION_STRING = ("AzureServiceBus", "connection_string")
    AZURE_SERVICE_BUS_QUEUE_NAME = ("AzureServiceBus", "queue_name")
    TELEGRAM_BOT_TOKEN = ("TelegramBot", "token")

    @staticmethod
    def get_default(service_name: Self) -> str:
        default = {
            ConfigEnum.LOG_LEVEL: "INFO",
        }
        return default.get(service_name)

    def __str__(self):
        return self.value
