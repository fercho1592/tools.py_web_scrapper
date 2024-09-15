'''Exception for http services'''
from requests.exceptions import RequestException

class HttpServiceException(BaseException):
  def __init__(self, request_exception: RequestException) -> None:
    super().__init__()
