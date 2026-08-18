import argparse
import json
import os

import pika

from app.handlers.pdf_creator_queue_handler import PDFCreateQueueHandler
from app.handlers.queue_download_handler import DownloadQueueHandler
from app.handlers.webdav_queue_handler import WebDavQueueHandler
from contracts.enums.queue_enum import QueueNameEnum
from core.config.dependency_injection import build_container


class QueueMessageManager:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        rabbitmq_url = os.getenv(
            "RABBITMQ_URL",
            os.getenv(
                "RABBITMQ_HOST",
                "amqp://guest:guest@localhost:5672/",
            ),
        )
        self.connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        return self

    def listen(self, handler):
        if self.channel is None:
            raise RuntimeError("Queue connection not initialized.")

        def callback(ch, method, properties, body):
            try:
                payload = json.loads(body.decode("utf-8"))
                message = (
                    payload.get("message") if isinstance(payload, dict) else payload
                )
                if message is None:
                    message = payload
                handler.on_message(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as exc:  # pragma: no cover - queue error handling
                print(f"Error processing message for queue '{self.queue_name}': {exc}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
        print(f"[QueueListener] Listening on queue: {self.queue_name}")
        self.channel.start_consuming()


QUEUE_HANDLER_MAP = {
    QueueNameEnum.DOWNLOAD.value: DownloadQueueHandler,
    QueueNameEnum.PDF.value: PDFCreateQueueHandler,
    QueueNameEnum.WEBDAV.value: WebDavQueueHandler,
}


def build_queue_handler(queue_name: str):
    container = build_container()
    try:
        handler_type = QUEUE_HANDLER_MAP[queue_name]
    except KeyError as exc:
        raise ValueError(f"Unsupported queue: {queue_name}") from exc
    return container.resolve_factory(handler_type)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a queue listener for the selected queue."
    )
    parser.add_argument(
        "--queue",
        required=True,
        choices=QueueNameEnum.choices(),
        help="Queue name to listen to.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    queue_name = args.queue

    queue_handler = build_queue_handler(queue_name)
    queue_manager = QueueMessageManager(queue_name)
    queue_manager.connect()
    queue_manager.listen(queue_handler)


if __name__ == "__main__":
    main()
