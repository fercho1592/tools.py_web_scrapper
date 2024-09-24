'''Tools to fix strings'''

class FixStringsTools:
    @staticmethod
    def fix_string_for_path(path_to_fix:str) -> str:
        path_to_fix = path_to_fix.replace("ū", "uu")
        return path_to_fix
