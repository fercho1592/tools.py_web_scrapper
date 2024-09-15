'''Exception for http services'''

class HttpServiceException(Exception):
  def __init__(self, message) -> None:
    super().__init__(message)
