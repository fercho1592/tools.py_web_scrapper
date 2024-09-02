import urllib.request

import Infrastructure.MyLogger as MyLogger
__logger = MyLogger.GetLogger(__name__)

__headers__ = {'User-Agent': 'Mozilla/5.0'}

def GetHtmlFromUrl(webPage):
    req = urllib.request.Request(url=webPage, headers=__headers__)
    
    __logger.debug(f"Getting info from {webPage}")
    response = urllib.request.urlopen(req)
    __logger.debug(f"result {response.status} from  [{webPage}] ")

    result = str(response.read())

    return result