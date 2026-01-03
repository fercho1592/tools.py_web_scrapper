'''File to get the settings'''
import configparser

@DeprecationWarning
def read_config():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read("./config.ini")

    # Access values from the configuration file
    log_level = config.get("General", "log_level")
    e_manga_strategy = config.get("MangaStrategy", "e_manga_domain")
    tmh_manga_domain = config.get("MangaStrategy", "tmh_manga_domain")

    # Return a dictionary with the retrieved values
    config_values = {
      "log_level": log_level,
      "e_manga_domain": e_manga_strategy,
      "tmh_manga_domain": tmh_manga_domain,
    }

    return config_values

@DeprecationWarning
def read_azure_service_bus_config():
    config = configparser.ConfigParser()
    config.read("./config.ini")

    connection_string = config.get("AzureServiceBus", "connection_string")
    queue_name = config.get("AzureServiceBus", "queue_name")

    return {
        "connection_string": connection_string,
        "queue_name": queue_name
    }

@DeprecationWarning
def read_telegram_bot_config():
    config = configparser.ConfigParser()
    config.read("./config.ini")

    bot_token = config.get("TelegramBot", "token")

    return {
        "bot_token": bot_token
    }


from feature_interfaces.protocols.config_protocol import ConfigServiceProtocol
from feature_interfaces.enums.settings_enum import ConfigEnum
from os import environ

class ConfigParserService(ConfigServiceProtocol):
    def __init__(self):
        super().__init__()
        self.file_path = "./config.ini"


    def get_config_value(self, service_name: ConfigEnum) -> str:
        config = configparser.ConfigParser()
        config.read(self.file_path)
        section, key = service_name.value
        return config.get(section, key)

class EnvironConfig(ConfigServiceProtocol):
    def __init__(self):
        pass

    def get_config_value(self, service_name: ConfigEnum) -> str:
        section, key = service_name.value
        service_name_str = f"{section.upper()}_{key.upper()}"
        value = environ.get(service_name_str)
        return value if value is not None else ConfigEnum.get_default(service_name)
