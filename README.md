## Installation

'''
pip3 install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r Requirements.txt
'''

## How use it
### Download queue file
use a file to create a queue to downloads you mangas


Each line in the file is a download, it have to has the url (index or first page), the name of the folder that is going to be download and the page number to start download separates by "|" element 

### Configurations
'''
[General]
debug = True
log_level = info

[MangaStrategy]
e_manga_domain = url_page
tmh_manga_domain = url_page

'''

### Common errors 

- https://medium.com/@yen.hoang.1904/resolve-issue-ssl-certificate-verify-failed-when-trying-to-open-an-url-with-python-on-macos-46d868b44e10