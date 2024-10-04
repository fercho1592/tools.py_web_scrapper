'''Tools to fix strings'''
import re
from unicodedata import normalize

class FixStringsTools:
    @staticmethod
    def fix_string_for_path(string:str) -> str:
        path_to_fix = string
        path_to_fix = path_to_fix.replace("ū", "uu")
        path_to_fix = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", path_to_fix), 0, re.I
        )
        path_to_fix = normalize( 'NFC', path_to_fix)

        return path_to_fix
    
    @staticmethod
    def normalize_string(text: str) -> str:
        result = normalize("NFD",text)\
            .replace("♥","")
        return result
