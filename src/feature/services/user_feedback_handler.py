from feature_interfaces.services.user_feedback_handler import (
    IUserFeedbackHandler,
    IProgressBar,
)
from tqdm import tqdm


class UserFeedbackHandler(IUserFeedbackHandler):
    def ShowMessage(self, message: str):
        print(message)

    def ShowMessageError(self, message: str):
        print(message)


class ProgressBar(IProgressBar):
    def __init__(self, itemsNumber: int, descriptionMessage: str):
        descriptionMessage = "Downloading images"
        self._progressBar = tqdm(range(itemsNumber), descriptionMessage, itemsNumber)

    def SetCurrentProcess(self, currentItemNumber: int) -> None:
        self._progressBar.update(currentItemNumber)

    def NextItem(self) -> None:
        self._progressBar.update()
