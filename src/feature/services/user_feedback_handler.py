from feature_interfaces.services.user_feedback_handler import IUserFeedbackHandler
from feature_interfaces.services.error_handler import IErrorHandler
from logging import Logger
from abc import ABC
from tqdm import tqdm

class UserFeedbackHandler(IUserFeedbackHandler):
    def __init__(self, elementName: str, itemsNumber:int, errorHandler: IErrorHandler, logger: Logger):
        self._progressBar = tqdm(range(itemsNumber), "Downloading images", itemsNumber)
        self._logger = logger
        self._elementName = elementName
        self._errorHandler = errorHandler

    def SetCurrentProcess(self,currentItemNumber:int) -> None:
        self._progressBar.update(currentItemNumber)

    def NextItem(self) -> None:
        self._progressBar.update()

    def ShowMessage(self, message: str):
        self._progressBar.write(message)
        self._logger.info(message)

    def ShowErrorMessage(self, message: str) -> None:
        self._progressBar.write(message)
        self._errorHandler.SaveDownloadError(message)