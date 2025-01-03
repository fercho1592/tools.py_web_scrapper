from feature_interfaces.services.file_manager import IFileManager
from abc import ABC, abstractmethod

class IImageEditorService(ABC):
    @abstractmethod
    def convert_image(
        self,
        folder_manager: IFileManager,
        image_name:str,
        new_image_name:str,
        destinyFolder: IFileManager
    ):
        pass
    
    @abstractmethod
    def get_image_size(
      self,
      folder_manager,
      image_name
    ) -> tuple[float, float]:
        pass

