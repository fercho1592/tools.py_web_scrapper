'''Code to read download queue file'''
import os
from typing import Self

class QueueItem:
    '''Classs to represent an item to download'''
    def __init__(self, manga_url, path, page_number=0, pdf_only = False) -> None:
        self.manga_url = manga_url
        self.folder_name = path
        self.page_number = page_number
        self.pdf_name = f"{self.folder_name.split("/")[-1]}.pdf"
        self.pdf_only = pdf_only

    @staticmethod
    def QueueItemFromFile(line:str) -> Self:
        line_items= line.strip().split("|")

        return QueueItem(
            manga_url= line_items[0].strip().lower(),
            path= f"{get_default_folder()}/{line_items[1].strip()}",
            page_number= int(
                line_items[2].strip() if len(line_items) >= 3 and line_items[2].strip() else 0
            ),
            pdf_only = bool(line_items[3].strip() if len(line_items) >= 4 else 0)
        )


def get_default_folder():
    desktop_path_mangas = os.path\
        .normpath(os.path.expanduser("~/Desktop")) + "/Manga_downloads"
    if not os.path.exists(desktop_path_mangas):
        os.makedirs(desktop_path_mangas)
    return desktop_path_mangas

def read_queue() -> list[QueueItem]:
    tuplas = []
    with open("download-queue.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if linea.startswith("#") or linea.rstrip() == "":
                continue
            tuplas.append(QueueItem.QueueItemFromFile(linea))
    return tuplas