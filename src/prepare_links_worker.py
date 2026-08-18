import argparse
import re
import time
from pathlib import Path

import core.config.dependency_injection as IOT
from contracts.protocols.config_protocol import LoggerProtocol
from core.config.queue_reader import QueueItem
from manga.manga_scrapper_context import MangaScraper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read manga links from a file and prepare a queue-ready output file."
    )
    parser.add_argument(
        "source_file",
        nargs="?",
        default="links.txt",
        help="Path to a file containing manga links to process.",
    )
    parser.add_argument(
        "--output",
        default="temp-download-queue.txt",
        help="Output path for the prepared queue file.",
    )
    return parser.parse_args()


def main(
    source_file: str = "links.txt", output_file: str = "temp-download-queue.txt"
) -> None:
    path = Path(source_file)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    container = IOT.build_container()
    logger: LoggerProtocol = container.resolve_factory(LoggerProtocol, __name__)
    links = read_links_from_file(str(path))
    queue_list = []
    error_links = []

    for link in links:
        try:
            if any(item.MangaUrl == link for item in queue_list):
                logger.info(f"Skipping duplicate link: {link}")
                continue
            logger.info(f"Processing link: {link}")
            scrapper: MangaScraper = container.resolve_factory(MangaScraper, link)
            manga_data = scrapper.get_manga_data()
            time.sleep(2)
            if is_series(manga_data):
                manga_data["chapter_number"] = identify_chapter_number(manga_data)

            item = QueueItem(
                manga_url=link,
                path=create_path(manga_data),
                page_number=0,
                pdf_only=False,
            )
            queue_list.append(item)
        except Exception as e:
            logger.error(f"Error processing link {link}: {e}")
            error_links.append(link)
            continue

    queue_list = sorted(queue_list, key=lambda x: x.FolderName)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        for item in queue_list:
            file.write(f"{item.MangaUrl} | {item.FolderName}\n")

    error_path = output_path.with_name("error_links.txt")
    with error_path.open("w", encoding="utf-8") as file:
        for item in error_links:
            file.write(f"{item}\n")

    logger.info("Prepared %s queue entries in %s", len(queue_list), output_path)


def create_path(manga_data: dict) -> str:
    regex = re.compile(r"\([^)]*\)|\[[^\]]*\]")
    pdf_name = regex.sub("", manga_data.get("name")).strip()
    artist = manga_data.get("artist", None)
    groups = manga_data.get("groups", "None")
    artist = artist if artist else groups
    result_path = f"[{artist}]/{pdf_name}"
    result_path = (
        str(result_path)
        .replace("//", "-")
        .replace("\\", "-")
        .replace("|", "-")
        .replace("\n", "")
        .replace("~", "-")
        .replace("?", "")
        .replace("!", "")
    )

    return str(result_path).upper()


def is_series(manga_data: dict) -> bool:
    return False


def identify_chapter_number(manga_data: dict) -> str:
    return "1"


def read_links_from_file(file_path: str = "links.txt") -> list[str]:
    links = []
    num_re = re.compile(r"^\s*\d+\s*[\.\)\-]?\s*(.*)")
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            m = num_re.match(line)
            if m:
                line = m.group(1).strip()

            links.append(line.split("|")[0].strip())
    return links


if __name__ == "__main__":
    args = parse_args()
    main(args.source_file, args.output)
