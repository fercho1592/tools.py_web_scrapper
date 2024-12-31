'''Code to read download queue file'''
from typing import Self

class QueueItem:
    '''Classs to represent an item to download'''
    def __init__(self, manga_url, path, page_number = None, pdf_only = False) -> None:
        self.manga_url = manga_url
        self.folder_name = path
        self.page_number = page_number
        self.pdf_name = f"{self.folder_name.split("/")[-1]}.pdf"
        self.pdf_only = 1
        self.download_files = not pdf_only

    @staticmethod
    def QueueItemFromFile(line:str):
        line_items= line.strip().split("|")

        sPageNumber = line_items[2].strip() if len(line_items) > 3 else None

        return QueueItem(
            manga_url= line_items[0].strip().lower(),
            path= line_items[1].strip(),
            page_number= int(sPageNumber) if sPageNumber else None,
            pdf_only = bool(line_items[3].strip() if len(line_items) >= 4 else 0)
        )

def read_queue() -> list[QueueItem]:
    tuplas:list[QueueItem] = []
    with open("download-queue.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if linea.startswith("#") or linea.rstrip() == "":
                continue
            tuplas.append(QueueItem.QueueItemFromFile(linea))
    return tuplas