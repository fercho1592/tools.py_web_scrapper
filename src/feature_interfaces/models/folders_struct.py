from dataclasses import dataclass
from os import path

WORKING_FOLDER = path.normpath(path.expanduser("~/Desktop")) + "/Manga_downloads"


@dataclass
class FolderPath:
    relative_path: str
    full_path: str

    def __init__(self, root_path: str, relative_path: str) -> None:
        self.root_path = root_path
        self.relative_path = relative_path
        self.full_path = path.abspath(relative_path)

    def get_file_path(self, file_name: str) -> str:
        return path.join(self.full_path, file_name)


@dataclass
class MangaFoldersStruct:
    def __init__(self, *manga_folder_path: list[str]) -> None:
        #  - for download images
        self.download_folder = FolderPath(
            root_path=path.join(WORKING_FOLDER, "download"),
            relative_path=path.join(WORKING_FOLDER, "download", *manga_folder_path),
        )
        #  - for images converted
        self.converted_folder = FolderPath(
            root_path=path.join(WORKING_FOLDER, "converted"),
            relative_path=path.join(WORKING_FOLDER, "converted", *manga_folder_path),
        )
        #  - for final pdf and
        self.pdf_folder = FolderPath(
            root_path=path.join(WORKING_FOLDER, "pdfs"),
            relative_path=path.join(WORKING_FOLDER, "pdfs", *manga_folder_path, ".."),
        )
        #  - for final pdf and
        self.dav_folder = FolderPath(
            root_path="_/Manga_downloads/",
            relative_path=path.join("_/Manga_downloads/", *manga_folder_path, ".."),
        )
        self.dav_folder.full_path = self.dav_folder.relative_path
        #  - for error logs
        self.error_log_folder = FolderPath(
            root_path=path.join(WORKING_FOLDER, "error_logs"),
            relative_path=path.join(WORKING_FOLDER, "error_logs", *manga_folder_path),
        )
