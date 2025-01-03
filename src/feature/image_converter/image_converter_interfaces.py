from feature_interfaces.services.file_manager import IFileManager
from abc import ABC

class IImageEditorService(ABC):
    def convert_image(
        self,
        folder_manager: IFileManager,
        image_name:str,
        new_image_name:str,
        dest_path = "./converted_to_jpg"
    ):
        pass

    def get_image_size(
      self,
      folder_manager,
      image_name
    ) -> tuple[float, float]:
        pass

