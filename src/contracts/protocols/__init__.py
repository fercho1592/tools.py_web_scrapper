"""Protocols contract wrappers."""

from contracts.protocols import (
    config_protocol as config_protocol,
    factory_protocol as factory_protocol,
    queue_handler_protocol as queue_handler_protocol,
)

__all__ = [
    "config_protocol",
    "factory_protocol",
    "queue_handler_protocol",
]
