from feature_interfaces.services.user_feedback_handler import IUserFeedbackHandler, IProgressBar
from feature_interfaces.services.error_handler import IErrorHandler
from tqdm import tqdm

class UserFeedbackHandler(IUserFeedbackHandler):
    def __init__(self, elementName: str, errorHandler: IErrorHandler):
        self._elementName = elementName
        self.ErrorHandler = errorHandler

    def ShowMessage(self, message: str):
        print(message)

    def ShowDownloadError(self, message: str, item: int, totalItems:int, ex: Exception):
        print(message)
        self.ErrorHandler.SaveDownloadError(message, item, totalItems, ex)

    def ShowMessageError(self, message: str, ex: Exception):
        print(message)
        self.ErrorHandler.SaveMessageError(message, ex)

    def CreateProgressBar(self, itemsNumber: int, descriptionMessage: str) -> IProgressBar:
        return ProgressBar(itemsNumber, descriptionMessage)

class ProgressBar(IProgressBar):
    def __init__(self, itemsNumber: int, descriptionMessage: str):
        descriptionMessage = "Downloading images"
        self._progressBar = tqdm(range(itemsNumber), descriptionMessage , itemsNumber)

    def SetCurrentProcess(self,currentItemNumber:int) -> None:
        self._progressBar.update(currentItemNumber)

    def NextItem(self) -> None:
        self._progressBar.update()
