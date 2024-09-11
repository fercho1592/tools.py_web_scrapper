'''Code to read download queue file'''

def read_queue() -> list[tuple[str, str, str]]:
  tuplas = []
  with open("download-queue.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
      elementos:list[str] = linea.strip().split("|")

      tupla = tuple(
          elementos[0].strip(),
          elementos[1].strip(),
          elementos[2].strip()
        )
      tuplas.append(tupla)
  return tuplas
