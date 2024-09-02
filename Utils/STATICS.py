class CommonAttr():
    HREF = 'href'
    CLASS = 'class'
    ID = 'id'
    NAME = 'name'
    STYLE = 'style'
    SRC = 'src'

    def GetCommonAttr():
        return [CommonAttr.SRC,
                CommonAttr.HREF,
                CommonAttr.CLASS, 
                CommonAttr.ID, 
                CommonAttr.NAME, 
                CommonAttr.STYLE]
    
class CommonTags():
    ANCHOR = 'a'
    TR = 'tr'
    SPAM = 'span'