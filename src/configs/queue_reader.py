'''Code to read download queue file'''
import os

def read_queue() -> list[list[str, str, str]]:
  tuplas = []
  with open("download-queue.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
      if linea.startswith("#") or linea.rstrip() == "":
        continue
      item:list[str] = linea.strip().split("|")
      desktop_path_mangas = os.path.normpath(os.path.expanduser("~/Desktop")) + "/Manga_downloads"
      if not os.path.exists(desktop_path_mangas):
        os.makedirs(desktop_path_mangas)

      url = item[0].strip()
      path = f"{desktop_path_mangas}/{item[1].strip()}"
      init_page = int(item[2].strip() if len(item) >= 3 and item[2].strip() else 0)
      pdf_name = item[3].strip() if len(item) >= 4 and item[3].strip() else None
      only_pdf = bool(item[4].strip() if len(item) >= 5 else 0)

      tupla = ( url, path, init_page, pdf_name, only_pdf)
      tuplas.append(tupla)
  return tuplas

