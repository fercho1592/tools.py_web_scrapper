'''Service to get html info from an url'''
import requests
import configs.my_logger as my_logger
from exceptions.http_service_exception import HttpServiceException
from feature_interfaces.services.http_service import IHttpService

__logger = my_logger.get_logger(__name__)
DEFAULT_HEADERS = {
  "User-Agent": "Mozilla/5.0 \
    (Macintosh; Intel Mac OS X 10_11_5) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/50.0.2661.102 Safari/537.36"
}

class HttpService(IHttpService):
    def __init__(self):
        self._headers = DEFAULT_HEADERS

    def GetHtmlFromUrl(self, web_page: str):
        try:
            response = requests.get(web_page, headers= self._headers, timeout= 10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise HttpServiceException(f"Error al obtener la url {web_page}") from e

    def DownloadImageFromUrl(self, url: str, imageName: str ,to_folder: str):
        try:
            response = requests.get(url, stream=True, headers= self._headers, timeout= 10)

            response.raise_for_status()

            with open(to_folder, "wb") as out_file:
                for chunk in response.iter_content(1024):
                    out_file.write(chunk)

            __logger.debug("Imagen descargada correctamente a: %s", to_folder)

        except requests.exceptions.RequestException as ex:
            raise HttpServiceException(f"Error al descargar la imagen: {url}") from ex

    def SetHeaders(self, headers: dict[str, str]):
        if headers is None or len(headers) == 0:
            return

        if self._headers is None:
            self._headers = {}
        self._headers.update(headers)
