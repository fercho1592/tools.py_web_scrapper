import re
from unicodedata import normalize

class FixStringsTools:
    @staticmethod
    def FixStringForPath(string:str) -> str:
        path_to_fix = string
        path_to_fix = path_to_fix.replace("ū", "uu")
        path_to_fix = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", path_to_fix), 0, re.I
        )
        path_to_fix = normalize("NFC", path_to_fix)

        return path_to_fix

    @staticmethod
    def NormalizeString(text: str) -> str:
        result = normalize("NFD",text)\
            .replace("♥","")
        return result

    @staticmethod
    def ConvertString(text:str)-> str:
        if len(text) == 0:
            return None

        return text.strip()
