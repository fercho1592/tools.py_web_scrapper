class QueueItem:
    def __init__(self, manga_url: str, path: str, page_number:int = None, pdf_only:bool = False) -> None:
        self.MangaUrl:str = manga_url.rstrip()
        self.FolderName:str = path.rstrip()
        self.PageNumber:int = page_number
        self.PdfName:str = f"{self.FolderName.rstrip().split("/")[-1]}.pdf"
        self.PdfOnly:bool = True
        self.DownloadFiles:bool = not pdf_only

    @staticmethod
    def QueueItemFromFile(line:str):
        line_items= line.strip().split("|")

        sPageNumber = line_items[2].strip() if len(line_items) > 3 else None

        return QueueItem(
            manga_url= line_items[0].strip().lower(),
            path= line_items[1].strip(),
            page_number= int(sPageNumber) if sPageNumber else 0,
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
