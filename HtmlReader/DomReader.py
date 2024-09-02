from Utils.STATICS import CommonAttr
import Infrastructure.MyLogger as MyLogger

class DomComponent:
    def __init__(self, components):
        self.__components__ = components

    def GetByTags(self, tagName):
        return [comp for comp in self.__components__ if tagName == comp.tag]
    
    def GetByAttrs(self, attr, valule = None):
        return [comp for comp in self.__components__ if comp.HasAttr(attr, valule)]
    
class HtmlComponent():
    def __init__(self, tag, attrs, parent = None):
        self.tag = tag
        self.attrs = attrs
        self.parent = parent
        self.children = []
        self.value = None

    def SetValue(self, value):
        self.value = value

    def getValue(self): return self.value

    def GetId(self):
        idAttr = [attr for attr in self.attrs if attr[0] == CommonAttr.ID]
        return idAttr[0][1] if len(idAttr) > 0 else None
    
    def AddChildren(self, child):
        self.children.append(child)

    def HasAttr(self, attr, value = None):
        for atribute in self.attrs:
            if atribute[0] != attr:
                continue
            if value != None and atribute[1] != value:
                continue

            return True
        return False
    
    def GetAttrValue(self, attr):
        for atribute in self.attrs:
            if atribute[0] != attr:
                continue

            return atribute[1]
        return None
    
    def GetChildrenByTag(self, tagName, attr = None, value = None):
        result = []
        for child in self.children:
            if(child.tag == tagName and attr == None):
                result.append(child)
            elif(child.tag == tagName and (attr != None and child.HasAttr(attr, value))):
                result.append(child)

            result.extend(child.GetChildrenByTag(tagName, attr, value))

        return result
