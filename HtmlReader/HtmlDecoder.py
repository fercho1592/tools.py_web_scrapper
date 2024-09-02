from html.parser import HTMLParser
from HtmlReader.DomReader import HtmlComponent, DomComponent

class HtmlDecoder(HTMLParser):
    def SetHtml(self, domHtml):
        self.Components = []
        self.lastOpen = []
        self.feed(domHtml)

    def handle_starttag(self, tag, attrs):
        lastComponent = self.lastOpen[-1] if len(self.lastOpen) > 0 else None
        newComponent = HtmlComponent(tag, attrs, lastComponent)
        if(lastComponent is not None):
            lastComponent.AddChildren(newComponent)

        self.Components.append(newComponent)
        self.lastOpen.append(newComponent)

    def handle_endtag(self, tag):
        lastOpen = self.lastOpen[-1]
        self.lastOpen.remove(lastOpen)

    def handle_data(self, data):
        if(len(self.lastOpen) == 0): return
        component = self.lastOpen[-1]
        component.SetValue(data)

    def GetDomComponent(self):
        return DomComponent(self.Components)
