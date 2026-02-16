import asyncio
import glob
import os
import configs.dependency_injection as IOT
from feature_interfaces.models.folders_struct import MangaFoldersStruct
from handler.webdav_handler import WebDavHandler, WebDavCommand


async def main():
    container = IOT.build_container()
    webdav_handler: WebDavHandler = container.resolve(WebDavHandler)
    pdf_files = get_all_pdfs_files()

    for pdf_file_path in pdf_files:
        pdf_name = pdf_file_path.split("/")[-1]
        relative_path = os.path.relpath(
            pdf_file_path, "/home/fercho1592/Desktop/Manga_downloads/pdfs/"
        )
        relative_path = relative_path.replace("\\", "/")
        manga_folders = MangaFoldersStruct(relative_path)

        pdf_file_path = manga_folders.pdf_folder
        webdav_path = manga_folders.dav_folder

        try:
            await webdav_handler.handle(
                WebDavCommand(
                    manga_name=pdf_name,
                    pdf_path=pdf_file_path,
                    dav_path=webdav_path,
                )
            )
        except Exception as e:
            print(f"Error al subir el archivo {relative_path}: {e}")
            continue


def get_all_pdfs_files():
    pdf_files = glob.glob(
        "/home/fercho1592/Desktop/Manga_downloads/pdfs/**/*.pdf", recursive=True
    )
    return pdf_files


if __name__ == "__main__":
    asyncio.run(main())
