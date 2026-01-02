from typing import Protocol
from feature_interfaces.enums.settings_enum import ConfigEnum


class ConfigServiceProtocol(Protocol):
    def get_config_value(self, service_name: ConfigEnum) -> str: ...
