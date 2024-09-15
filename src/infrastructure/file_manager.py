'''Code to read download queue file'''

def read_queue() -> list[list[str, str, str]]:
  tuplas = []
  with open("download-queue.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
      if linea.startswith("#") or linea.rstrip() == "":
        continue
      item:list[str] = linea.strip().split("|")

      tupla = (
          item[0].strip(),
          item[1].strip(),
          int(item[2] if len(item) >= 3 else 0),
          item[3] if len(item) >= 4 else None

        )
      tuplas.append(tupla)
  return tuplas

