#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
from typing import Iterable
from uuid import uuid4

DEFAULT_QUEUE_NAME = "download"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish entries from a queue text file into the RabbitMQ download queue."
    )
    parser.add_argument(
        "--file",
        default="download-queue.txt",
        help="Path to the queue file to publish. Default: download-queue.txt",
    )
    parser.add_argument(
        "--queue",
        default=os.getenv("RABBITMQ_DOWNLOAD_QUEUE", DEFAULT_QUEUE_NAME),
        help="RabbitMQ queue name. Defaults to the download queue.",
    )
    parser.add_argument(
        "--rabbitmq-url",
        default=os.getenv(
            "RABBITMQ_URL",
            os.getenv(
                "RABBITMQ_HOST", "amqp://web_scrapper_user:t3st1ng@192.168.3.39:5672/"
            ),
        ),
        help="RabbitMQ connection URL.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print queued messages without publishing to RabbitMQ.",
    )
    return parser.parse_args()


def parse_queue_entries(file_path: str | Path) -> list[dict]:
    entries: list[dict] = []
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            cleaned = line.strip()
            if not cleaned or cleaned.startswith("#"):
                continue

            parts = [part.strip() for part in cleaned.split("|")]
            if len(parts) < 2:
                raise ValueError(f"Invalid queue entry on line {line_number}: '{line}'")

            manga_url, download_folder = parts[0], parts[1]
            entries.append(
                {
                    "id": str(uuid4()),
                    "queue_name": DEFAULT_QUEUE_NAME,
                    "messageCommand": {
                        "manga_url": manga_url,
                        "download_folder": download_folder,
                        "queue_name": DEFAULT_QUEUE_NAME,
                        "next_queue": "pdf",
                        "chapters": [],
                    },
                    "errorLog": [],
                }
            )

    return entries


def publish_entries(
    entries: Iterable[dict], queue_name: str, rabbitmq_url: str
) -> None:
    try:
        import pika
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "pika is required to publish messages to RabbitMQ. Install project dependencies first."
        ) from exc

    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    try:
        for entry in entries:
            payload = json.dumps(entry, ensure_ascii=False).encode("utf-8")
            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=payload,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json",
                ),
            )
            print(
                f"Published to '{queue_name}': {entry['messageCommand']['manga_url']}"
            )
    finally:
        connection.close()


def main() -> None:
    args = parse_args()
    entries = parse_queue_entries(args.file)

    if args.dry_run:
        for entry in entries:
            print(json.dumps(entry, ensure_ascii=False))
        print(
            f"Dry run complete. {len(entries)} entries prepared for queue '{args.queue}'."
        )
        return

    publish_entries(entries, args.queue, args.rabbitmq_url)
    print(f"Published {len(entries)} queue entries to '{args.queue}'.")


if __name__ == "__main__":
    main()
