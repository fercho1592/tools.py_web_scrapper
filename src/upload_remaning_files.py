from webdav4.client import Client
import glob
import os
import configs.dependency_injection as IOT
from feature_interfaces.models.folders_struct import FolderPath
from feature.web_driver. import 
from feature_interfaces.services.webdav_service import WebDAVService

def main():
    container = IOT.build_container()
    webdav_service: WebDAVService = container.resolve(WebDAVService)



pdf_files = glob.glob(
    "/home/fercho1592/Desktop/Manga_downloads/pdfs/**/*.pdf", recursive=True
)
for pdf_file in pdf_files:
    try:
        # get relative path
        relative_path = os.path.relpath(
            pdf_file, "/home/fercho1592/Desktop/Manga_downloads/pdfs/"
        )
        # replace backslashes with forward slashes
        relative_path = relative_path.replace("\\", "/")
        remote_path = f"_/Manga_downloads/{relative_path}"
        if client.exists(remote_path):
            print(f"El archivo {relative_path} ya existe en el servidor WebDAV.")
            os.remove(pdf_file)
            print(f"Archivo {relative_path} eliminado localmente.")
        else:
            if not client.exists(os.path.dirname(remote_path)):
                create_remote_dirs(client, remote_path)
            client.upload_file(from_path=pdf_file, to_path=remote_path)
            print(f"Archivo {relative_path} subido exitosamente al servidor WebDAV.")
    #         return
    except Exception as e:
        print(f"Error al subir el archivo {relative_path}: {e}")
        continue
#         return
#     return

if __name__ == "__main__":
    main()