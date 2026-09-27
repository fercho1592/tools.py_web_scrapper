from dataclasses import dataclass
from threading import Thread
from typing import Any, Protocol


@dataclass
class QueueMessage[TCommand]:
    id: str
    queue_name: str
    messageCommand: dict[str, Any]
    errorLog: list[str]

    def to_command(self, command_class: type[TCommand]) -> TCommand:
        return command_class(**self.messageCommand)


class QueueHandlerProtocol[TCommand](Protocol):
    def __init__(self, queue_name: str, next_queue: str):
        self.queue_name = queue_name
        self.next_queue = next_queue

    def on_message(self, payload: dict[str, Any]) -> Thread:
        pass
