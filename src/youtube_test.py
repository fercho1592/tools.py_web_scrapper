import yt_dlp
from core.config.queue_reader import read_video_queue, QueueItem
from contracts.models.folders_struct import VideoFoldersStruct


def descargar_video(item: QueueItem):
    videoFolder = VideoFoldersStruct(item.FolderName)

    ydl_opts = {
        # 'bestvideo+bestaudio/best' asegura la máxima calidad
        "format": "bestvideo+bestaudio/best",
        # Nombre del archivo de salida
        "outtmpl": f"{videoFolder.download_folder.full_path}.%(ext)s",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Iniciando descarga...")
            ydl.download([item.MangaUrl])
            print("\n¡Descarga completada con éxito!")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    for item in read_video_queue():
        descargar_video(item)
