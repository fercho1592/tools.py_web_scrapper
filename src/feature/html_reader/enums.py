'''Enums to Attrs and Tags'''
from enum import Enum

class CommonAttrs(Enum):
    HREF= "href"
    CLASS = "class"
    ID = "id"
    NAME = "name"
    STYLE = "style"
    SRC = "src"
    SELECTED = "selected"
    DATA_ORIGINAL = "data-original"

class CommonTags(Enum):
    ANCHOR = "a"
    TR = "tr"
    TD = "td"
    SPAN = "span"
    H3 = "h3"
    H1 = "h1"
    OPTION = "option"
    IMG = "img"
    I = "i"
    UL = "ul"
    LI = "li"
