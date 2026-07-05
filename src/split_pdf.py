import fitz  # Así se importa PyMuPDF


def dividir_pdf_pesado(ruta_entrada, from_page, to_page, prefijo_salida, file_name):
    # 1. Abrir el PDF original
    doc = fitz.open(ruta_entrada)
    total_paginas = len(doc)
    to_page = to_page if to_page > 0 else total_paginas

    print(
        f"Total de páginas: {total_paginas}. Dividiendo en partes de {to_page} páginas..."
    )

    # --- PARTE 1 (Páginas 0 a la mitad) ---
    doc_parte1 = fitz.open()  # Crear un PDF vacío
    doc_parte1.insert_pdf(doc, from_page=from_page, to_page=to_page - 1)
    # Guardamos optimizando el espacio y limpiando basura interna
    doc_parte1.save(f"{prefijo_salida}/{file_name}", garbage=4, deflate=True)
    doc_parte1.close()
    print("¡ guardada y optimizada!")

    doc.close()


if __name__ == "__main__":
    original_pdf = "/home/fercho1592/Desktop/Manga_downloads/pdfs/[EGGYS]/SAO STORY VOL.45 - 93.pdf"  # Ruta del PDF original
    to_page_to_split = 918  # Número de páginas por cada archivo resultante
    output_path = "/home/fercho1592/Desktop/Manga_downloads/pdfs/[EGGYS]"
    pdf_name = "SAO STORY VOL.45 - 68.pdf"
    # Prefijo para los archivos resultantes
    # Ejemplo de uso: Divide un PDF en partes de 5 páginas cada una
    dividir_pdf_pesado(original_pdf, 0, to_page_to_split, output_path, pdf_name)

    from_page_to_split = 918  # Número de páginas por cada archivo resultante
    output_path = "/home/fercho1592/Desktop/Manga_downloads/pdfs/[EGGYS]"
    pdf_name = "SAO STORY VOL.69 - 93.pdf"
    # Prefijo para los archivos resultantes
    # Ejemplo de uso: Divide un PDF en partes de 5 páginas cada una
    dividir_pdf_pesado(original_pdf, from_page_to_split, -1, output_path, pdf_name)
