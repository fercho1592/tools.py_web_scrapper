'''Service to get html info from an url'''

import urllib.request

import infrastructure.my_logger as my_logger
__logger = my_logger.GetLogger(__name__)

__headers__ = {"User-Agent": "Mozilla/5.0"}

def get_html_from_url(web_page):
  req = urllib.request.Request(url=web_page, headers=__headers__)

  __logger.debug("Getting info from %s", web_page )
  response = urllib.request.urlopen(req)
  __logger.debug("result %s from  [%s] ", response.status, web_page)

  result = str(response.read())

  return result
