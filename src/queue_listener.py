import argparse
import json
import os
import traceback
from functools import partial
from threading import Thread
from time import time
from typing import Any

import pika

from app.handlers.pdf_creator_queue_handler import PDFCreateQueueHandler
from app.handlers.queue_download_handler import DownloadQueueHandler
from app.handlers.split_folders_queue_handler import SplitFoldersQueueHandler
from app.handlers.webdav_queue_handler import WebDavQueueHandler
from contracts.enums.queue_enum import QueueNameEnum
from core.config.dependency_injection import build_container

DEFAULT_QUEUE_MAX_THREADS = 1
ERROR_QUEUE_NAME = QueueNameEnum.ERRORS.value
QUEUE_MAX_THREADS = {
    QueueNameEnum.DOWNLOAD.value: 1,
    QueueNameEnum.SPLIT_FOLDERS.value: 1,
    QueueNameEnum.PDF.value: 1,
    QueueNameEnum.WEBDAV.value: 1,
}


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
        self.channel.queue_declare(queue=ERROR_QUEUE_NAME, durable=True)
        return self

    def _publish_message(self, queue_name: str, payload: Any) -> None:
        if self.channel is None:
            return

        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json",
            ),
        )

    def _publish_error(
        self,
        message: Any,
        error: Exception,
        *,
        traceback_info: str,
    ):
        if self.channel is None:
            return

        error_payload = {
            "origin_queue": self.queue_name,
            "message": message,
            "error": str(error),
            "traceback": traceback_info,
            "timestamp": time(),
        }

        self._publish_message(ERROR_QUEUE_NAME, error_payload)

    def _handle_worker_failure(
        self, channel, delivery_tag: int, message: Any, error: Any
    ):
        if self.connection is None:
            return

        def nack_with_error_publish() -> None:
            failure = (
                error
                if isinstance(error, Exception)
                else RuntimeError(str(error) if error is not None else "Worker failed")
            )

            try:
                traceback_info = ""
                if isinstance(error, dict):
                    traceback_info = str(error.get("traceback", ""))
                self._publish_error(message, failure, traceback_info=traceback_info)
            except (
                TypeError,
                ValueError,
                RuntimeError,
                OSError,
                pika.exceptions.AMQPError,
            ) as publish_error:  # pragma: no cover - queue error fallback
                print(
                    f"Error publishing failed worker message for queue "
                    f"'{self.queue_name}': {publish_error}"
                )
            channel.basic_nack(delivery_tag=delivery_tag, requeue=False)

        self.connection.add_callback_threadsafe(nack_with_error_publish)

    def listen(self, handler):
        if self.channel is None:
            raise RuntimeError("Queue connection not initialized.")

        max_threads = max(
            1,
            QUEUE_MAX_THREADS.get(self.queue_name, DEFAULT_QUEUE_MAX_THREADS),
        )

        def callback(ch, method, properties, body):
            payload: Any = None
            message: Any = body.decode("utf-8", errors="replace")
            try:
                del properties
                payload = json.loads(body.decode("utf-8"))
                message = (
                    payload.get("message") if isinstance(payload, dict) else payload
                )
                if message is None:
                    message = payload

                result = handler.on_message(message)
                if isinstance(result, Thread):
                    # Ack after worker completion so prefetch_count enforces
                    # max concurrent messages per queue.
                    self._ack_after_thread(
                        result,
                        ch,
                        method.delivery_tag,
                        message,
                    )
                else:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
            except (
                json.JSONDecodeError,
                UnicodeDecodeError,
                TypeError,
                ValueError,
                KeyError,
                AttributeError,
                RuntimeError,
                OSError,
                pika.exceptions.AMQPError,
            ) as exc:  # pragma: no cover - queue error handling
                print(f"Error processing message for queue '{self.queue_name}': {exc}")
                try:
                    message_to_send = payload if payload is not None else message
                    self._publish_error(
                        message_to_send,
                        exc,
                        traceback_info=traceback.format_exc(),
                    )
                except (
                    TypeError,
                    ValueError,
                    RuntimeError,
                    OSError,
                    pika.exceptions.AMQPError,
                ) as publish_error:  # pragma: no cover - queue error fallback
                    print(
                        f"Error publishing failed message for queue "
                        f"'{self.queue_name}': {publish_error}"
                    )
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        self.channel.basic_qos(prefetch_count=max_threads)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
        print(
            f"[QueueListener] Listening on queue: {self.queue_name} "
            f"(max_threads={max_threads})"
        )
        self.channel.start_consuming()

    def _ack_after_thread(
        self,
        worker: Thread,
        channel,
        delivery_tag: int,
        message: Any,
    ) -> None:
        def wait_and_ack() -> None:
            worker.join()
            if self.connection is None:
                return

            worker_error = getattr(worker, "_queue_error", None)
            if worker_error is not None:
                self._handle_worker_failure(
                    channel,
                    delivery_tag,
                    message,
                    worker_error,
                )
                return

            next_queue_message = getattr(worker, "_next_queue_message", None)
            if next_queue_message is not None:
                next_queue_name = next_queue_message.get("queue_name")
                if next_queue_name:
                    self._publish_message(next_queue_name, next_queue_message)

            ack_call = partial(channel.basic_ack, delivery_tag=delivery_tag)
            self.connection.add_callback_threadsafe(ack_call)

        Thread(target=wait_and_ack, daemon=True).start()


QUEUE_HANDLER_MAP = {
    QueueNameEnum.DOWNLOAD.value: DownloadQueueHandler,
    QueueNameEnum.SPLIT_FOLDERS.value: SplitFoldersQueueHandler,
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
