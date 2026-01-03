import unittest
from src.feature_interfaces.enums.settings_enum import ConfigEnum

class TestConfigEnum(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(ConfigEnum.LOG_LEVEL.value, ("General", "log_level"))
        self.assertEqual(ConfigEnum.E_MANGA_DOMAIN.value, ("MangaStrategy", "e_manga_domain"))
        self.assertEqual(ConfigEnum.TMH_MANGA_DOMAIN.value, ("MangaStrategy", "tmh_manga_domain"))
        self.assertEqual(ConfigEnum.AZURE_SERVICE_BUS_CONNECTION_STRING.value, ("AzureServiceBus", "connection_string"))
        self.assertEqual(ConfigEnum.AZURE_SERVICE_BUS_QUEUE_NAME.value, ("AzureServiceBus", "queue_name"))
        self.assertEqual(ConfigEnum.TELEGRAM_BOT_TOKEN.value, ("TelegramBot", "token"))

    def test_get_default(self):
        self.assertEqual(ConfigEnum.get_default(ConfigEnum.LOG_LEVEL), "INFO")
        self.assertIsNone(ConfigEnum.get_default(ConfigEnum.E_MANGA_DOMAIN))

    def test_str_method(self):
        self.assertEqual(str(ConfigEnum.LOG_LEVEL), str(("General", "log_level")))
        self.assertEqual(str(ConfigEnum.TELEGRAM_BOT_TOKEN), str(("TelegramBot", "token")))

if __name__ == "__main__":
    unittest.main()
