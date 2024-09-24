'''Exception for MangaScrapper'''
class MangaScrapperException(Exception):
    '''Custom Exception for manga scraper'''
    def __init__(self, url:str, page:int | None, max_page:int | None  ) -> None:
        is_index_page = page is None
        page_message = f"page ({page}/{max_page})"
        index_message = "index page"
        message = f"Error downloading [{url}] on {index_message if is_index_page else page_message}"
        super().__init__(message)
