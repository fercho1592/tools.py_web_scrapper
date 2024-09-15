'''Code to read download queue file'''

def read_queue() -> list[list[str, str, str]]:
  tuplas = []
  with open("download-queue.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
      if linea.startswith("#") or linea.rstrip() == "":
        continue
      elementos:list[str] = linea.strip().split("|")

      tupla = (
          elementos[0].strip(),
          elementos[1].strip(),
          int(elementos[2].strip())
        )
      tuplas.append(tupla)
  return tuplas

