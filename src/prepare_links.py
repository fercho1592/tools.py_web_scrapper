import re
from configs import dependency_injection as IOT
from configs.queue_reader import QueueItem
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature.manga_strategy.manga_scrapper_context import MangaScraper


def main() -> None:
    # initialize container and services
    container = IOT.build_container()
    logger: LoggerProtocol = container.resolve_factory(LoggerProtocol, __name__)
    links = read_links_from_file("links.txt")
    queue_list = []

    # Get a list of links

    # for each link
    for link in links:
        try:
            if [item for item in queue_list if item.MangaUrl == link]:
                logger.info(f"Skipping duplicate link: {link}")
                continue
            logger.info(f"Processing link: {link}")
            scrapper: MangaScraper = container.resolve_factory(MangaScraper, link)
            # get all metadata
            manga_data = scrapper.get_manga_data()
            # identify if is part of a series
            if is_series(manga_data):
                # identify chapter number
                manga_data["chapter_number"] = identify_chapter_number(manga_data)
            # Create queue item

            item = QueueItem(
                manga_url=link,
                path=create_path(manga_data),
                page_number=0,
                pdf_only=False,
            )
            # add to result list
            queue_list.append(item)
        except Exception as e:
            logger.error(f"Error processing link {link}: {e}")
            continue

    queue_list = sorted(queue_list, key=lambda x: x.FolderName)

    # serialize result list to file
    with open("temp-download-queue.txt", "w") as f:
        for item in queue_list:
            f.write(
                f"{item.MangaUrl}|{item.FolderName}|{item.PageNumber}|{item.PdfOnly}\n"
            )
    pass


def create_path(manga_data: dict) -> str:
    regex = re.compile(r"\([^)]*\)|\[[^\]]*\]")
    pdf_name = regex.sub("", manga_data.get("name")).strip() + ".pdf"
    # get artist
    artist = manga_data.get("artist", None)
    # get groups
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
    # logic to determine if manga is part of a series
    return False


def identify_chapter_number(manga_data: dict) -> str:
    # logic to identify chapter number from manga data
    return "1"


def read_links_from_file(file_path: str = "links.txt") -> list[str]:
    links = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                links.append(line.split(" ")[-1])
    return links


if __name__ == "__main__":
    main()
