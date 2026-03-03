import yt_dlp


def descargar_video(url):
    ydl_opts = {
        # 'bestvideo+bestaudio/best' asegura la máxima calidad
        "format": "bestvideo+bestaudio/best",
        # Nombre del archivo de salida
        "outtmpl": "%(title)s.%(ext)s",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Iniciando descarga...")
            ydl.download([url])
            print("\n¡Descarga completada con éxito!")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    # url = input("Introduce la URL del video de YouTube: ")
    # url = "https://www.youtube.com/watch?v=Kgo-PRi_aJw"

    url = "https://zoids.lat/filemooon/zoids-cc/1/master.m3u8"
    descargar_video(url)
