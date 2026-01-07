from feature_interfaces.models.folders_struct import FolderPath
from abc import ABC, abstractmethod

class IImageEditorService(ABC):
    @abstractmethod
    def convert_image(
        self,
        folder_manager: FolderPath,
        image_name:str,
        new_image_name:str,
        destinyFolder: FolderPath
    ):
        pass
    
    @abstractmethod
    def get_image_size(
      self,
      folder_manager: FolderPath,
      image_name: str
    ) -> tuple[float, float]:
        pass

