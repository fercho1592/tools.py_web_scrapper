"""Service to get html info from an url"""

import requests
from exceptions.http_service_exception import HttpServiceException
from feature_interfaces.protocols.config_protocol import LoggerProtocol
from feature_interfaces.services.http_service import IHttpService
from feature_interfaces.web_drivers.i_html_decoder import IHtmlDecoder
from os import path

from feature_interfaces.web_drivers.i_web_reader_driver import IWebReaderDriver

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 \
    (Macintosh; Intel Mac OS X 10_11_5) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/50.0.2661.102 Safari/537.36"
}


class HttpService(IHttpService):
    def __init__(
        self,
        logger: LoggerProtocol,
        html_decoder: IHtmlDecoder,
    ):
        self._headers = DEFAULT_HEADERS
        self._logger = logger
        self._html_decoder = html_decoder

    def GetHtmlFromUrl(self, web_page: str):
        try:
            response = requests.get(web_page, headers=self._headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise HttpServiceException(f"Error al obtener la url {web_page}") from e

    def DownloadImageFromUrl(self, url: str, imageName: str, to_folder: str):
        try:
            filePath = path.join(to_folder, imageName)
            response = requests.get(url, stream=True, headers=self._headers, timeout=10)

            response.raise_for_status()

            with open(filePath, "wb") as out_file:
                for chunk in response.iter_content(1024):
                    out_file.write(chunk)

            self._logger.debug("Imagen descargada correctamente a: %s", to_folder)

        except requests.exceptions.RequestException as ex:
            raise HttpServiceException(f"Error al descargar la imagen: {url}") from ex

    def SetHeaders(self, headers: dict[str, str]):
        if headers is None or len(headers) == 0:
            return

        if self._headers is None:
            self._headers = {}
        self._headers.update(headers)

    def GetDoomComponentFromUrl(self, url: str) -> IWebReaderDriver:
        html = self.GetHtmlFromUrl(url)
        self._html_decoder.set_html(html)
        return self._html_decoder.get_dom_component()
