from enum import Enum


class QueueNameEnum(str, Enum):
    DOWNLOAD = "download"
    PDF = "pdf"
    WEBDAV = "webdav"

    @classmethod
    def from_value(cls, value: str) -> "QueueNameEnum":
        normalized = (value or "").strip().lower()
        for queue_name in cls:
            if queue_name.value == normalized:
                return queue_name
        raise ValueError(f"Unsupported queue: {value}")

    @classmethod
    def choices(cls) -> list[str]:
        return [queue_name.value for queue_name in cls]
