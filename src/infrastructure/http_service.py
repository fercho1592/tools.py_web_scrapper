'''Service to get html info from an url'''
import requests
import infrastructure.my_logger as my_logger
__logger = my_logger.get_logger(__name__)
default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def get_html_from_url(web_page):
  try:
    response = requests.get(web_page, headers= default_headers, timeout= 10)
    response.raise_for_status()
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"Error al obtener el cuerpo: {e}")
    raise e


def download_image_from_url(url: str, to_folder: str, headers: dict[str, str] = None):
  try:
    if headers is None:
      headers = default_headers
    headers.update(default_headers)
    # Realiza una solicitud GET a la URL de la imagen
    response = requests.get(url, stream=True, headers= headers, timeout= 10)

    # Verifica si la solicitud fue exitosa (código de estado 200)
    response.raise_for_status()

    # Abre un archivo en modo escritura binaria para guardar la imagen
    with open(to_folder, "wb") as out_file:
      for chunk in response.iter_content(1024):
        out_file.write(chunk)

    __logger.debug("Imagen descargada correctamente a: %s", to_folder)

  except requests.exceptions.RequestException as e:
    __logger.error("Error al descargar la imagen: %r", e)
    raise e
