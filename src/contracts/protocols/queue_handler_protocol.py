from dataclasses import dataclass
from threading import Thread
from typing import Protocol


@dataclass
class QueueMessage[TCommand]:
    id: str
    queue_name: str
    messageCommand: TCommand
    errorLog: list[str]


class QueueHandlerProtocol[TCommand](Protocol):
    def __init__(self, queue_name: str, next_queue: str):
        self.queue_name = queue_name
        self.next_queue = next_queue

    def on_message(self, command: QueueMessage[TCommand]) -> Thread:
        pass
