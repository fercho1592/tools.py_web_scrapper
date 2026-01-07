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
        scrapper:MangaScraper = container.resolve_factory(MangaScraper, link)
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

    queue_list = sorted(queue_list, key=lambda x: x.path)

    # serialize result list to file
    with open("temp-download-queue.txt", "w") as f:
        for item in queue_list:
            f.write(f"{item.MangaUrl}|{item.FolderName}|{item.PageNumber}|{item.PdfOnly}\n")
    pass

def create_path(manga_data: dict) -> str:
    pdf_name = manga_data.get("title", "manga") + ".pdf"
    return str(pdf_name).upper()

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
