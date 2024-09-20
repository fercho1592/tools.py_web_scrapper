'''Module to read Html and parse to handled objects'''
from . import dom_reader
from . import html_decoder
from . import enums

__all__ = [
    dom_reader.DomElement.__name__,
    dom_reader.HtmlElement.__name__,
    html_decoder.HtmlDecoder.__name__,
    enums.CommonAttrs.__name__,
    enums.CommonTags.__name__
]
