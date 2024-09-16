from infrastructure.file_manager import FileDownloader
class IImageEditorService:
  def convert_image(
      self,
      folder_manager: FileDownloader,
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

