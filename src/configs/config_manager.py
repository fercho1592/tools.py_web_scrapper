'''File to get the settings'''
import configparser

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

def read_azure_service_bus_config():
    config = configparser.ConfigParser()
    config.read("./config.ini")

    connection_string = config.get("AzureServiceBus", "connection_string")
    queue_name = config.get("AzureServiceBus", "queue_name")

    return {
        "connection_string": connection_string,
        "queue_name": queue_name
    }

def read_telegram_bot_config():
    config = configparser.ConfigParser()
    config.read("./config.ini")

    bot_token = config.get("TelegramBot", "token")

    return {
        "bot_token": bot_token
    }
