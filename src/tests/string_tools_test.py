import pytest
from ..tools.string_path_fix import FixStringsTools

class Test:

    @pytest.mark.parametrize(("string", "expected"), [
        ("hello_world_ū", "hello_world_uu"),
        ("échos", "echos"),
        ("íchos", "ichos"),
        #("ñoño", "nono"),
    ])
    def test_fix_string_for_path(self, string, expected):
        assert FixStringsTools.FixStringForPath(string) == expected


    @pytest.mark.parametrize(("string", "expected"), [
        ("Sukininaru♥", "Sukininaru"),
    ])
    def test_normailize_string_gets_invalid_text_return_valid_text(self, string, expected):
        assert FixStringsTools.NormalizeString(string) == expected
