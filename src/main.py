'''Main code'''
import feature.manga_scrapper_context as manga_scrapper_context

if __name__ == "__main__":
  downloadQueue = []

  for item in downloadQueue:
    print("*************************************************")
    if item[2]:
      errorList = manga_scrapper_context.GetMangaFromIndex(
        item[0], manga_name= item[1], page = item[3])
    else:
      errorList = manga_scrapper_context.GetMangaFromPage(
        item[0], manga_name= item[1])

    if len(errorList[1]) > 0:
      print(f"Error in these images from [{errorList[0]}]", errorList[1])
      print("*************************************************")
