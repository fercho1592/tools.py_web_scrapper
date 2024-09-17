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
          int(item[2].strip() if len(item) >= 3 and item[2].strip() else 0),
          item[3].strip() if len(item) >= 4 and item[3].strip() else None,
          bool(item[4].strip() if len(item) >= 5 else 0),
        )
      tuplas.append(tupla)
  return tuplas

