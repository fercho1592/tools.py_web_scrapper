from webdav4.client import Client

# Configuramos la conexión
client = Client(
    base_url="http://192.168.3.39:8080/remote.php/dav/files/admin",
    auth=("admin", "59m5hvUFE!yRI0xP"),
)

# local_path = "/home/fercho1592/Desktop/Manga_downloads/pdfs/[AME ARARE]/-Toshoshitsu no Kanojo/vol 6_5.pdf"
# remote_path = "_/Manga_downloads/[AME ARARE]/-TOSHOSHITSU NO KANOJO/vol 6_5.pdf"
# if client.exists(remote_path):
#     print("El archivo ya existe en el servidor WebDAV.")
# else:
#     client.upload_file(from_path=local_path, to_path=remote_path)
#     print("Archivo subido exitosamente al servidor WebDAV.")

# get all pdf files in /home/fercho1592/Desktop/Manga_downloads/pdfs/**/*.pdf
import glob
import os


def create_remote_dirs(client: Client, remote_path):
    dirs = remote_path.split("/")
    path = ""
    for dir in dirs[:-1]:  # Exclude the file name
        path = os.path.join(path, dir)
        if not client.exists(path):
            client.mkdir(path)


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
