from dataclasses import dataclass
from os import path

WORKING_FOLDER_MANGA = path.normpath(path.expanduser("~/Desktop")) + "/Manga_downloads"
WORKING_FOLDER_VIDEO = path.normpath(path.expanduser("~/Desktop")) + "/Video_downloads"


@dataclass
class FolderPath:
    relative_path: str
    full_path: str

    def __init__(self, root_path: str, relative_path: str) -> None:
        self.root_path = root_path
        self.relative_path = relative_path
        self.full_path = path.abspath(relative_path)

    def get_file_path(self, file_name: str) -> str:
        return path.normpath(path.join(self.full_path, file_name))


@dataclass
class MangaFoldersStruct:
    def __init__(self, *manga_folder_path: list[str]) -> None:
        #  - for download images
        self.download_folder = FolderPath(
            root_path=fix_path(WORKING_FOLDER_MANGA, "download"),
            relative_path=fix_path(
                WORKING_FOLDER_MANGA, "download", *manga_folder_path
            ),
        )
        #  - for images converted
        self.converted_folder = FolderPath(
            root_path=fix_path(WORKING_FOLDER_MANGA, "converted"),
            relative_path=fix_path(
                WORKING_FOLDER_MANGA, "converted", *manga_folder_path
            ),
        )
        #  - for final pdf and
        self.pdf_folder = FolderPath(
            root_path=fix_path(WORKING_FOLDER_MANGA, "pdfs"),
            relative_path=fix_path(
                WORKING_FOLDER_MANGA, "pdfs", *manga_folder_path, ".."
            ),
        )
        #  - for final pdf and
        self.dav_folder = FolderPath(
            root_path="_/Manga_downloads/",
            relative_path=path.normpath(
                path.join("_/Manga_downloads/", *manga_folder_path, "..")
            ),
        )
        self.dav_folder.full_path = self.dav_folder.relative_path
        #  - for error logs
        self.error_log_folder = FolderPath(
            root_path=fix_path(WORKING_FOLDER_MANGA, "error_logs"),
            relative_path=fix_path(
                WORKING_FOLDER_MANGA, "error_logs", *manga_folder_path
            ),
        )


@dataclass
class VideoFoldersStruct:
    def __init__(self, *video_folder_path: list[str]) -> None:
        #  - for download videos
        self.download_folder = FolderPath(
            root_path=fix_path(WORKING_FOLDER_VIDEO, "download"),
            relative_path=fix_path(
                WORKING_FOLDER_VIDEO, "download", *video_folder_path
            ),
        )
        #  - for final videos and
        self.final_folder = FolderPath(
            root_path=fix_path(WORKING_FOLDER_VIDEO, "final_videos"),
            relative_path=fix_path(
                WORKING_FOLDER_VIDEO, "final_videos", *video_folder_path
            ),
        )
        #  - for error logs
        self.error_log_folder = FolderPath(
            root_path=fix_path(WORKING_FOLDER_VIDEO, "error_logs"),
            relative_path=fix_path(
                WORKING_FOLDER_VIDEO, "error_logs", *video_folder_path
            ),
        )


def fix_path(*str_path: list[str]):
    return path.normpath(path.join(*str_path))
