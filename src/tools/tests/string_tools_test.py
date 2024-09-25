import pytest
from ..string_path_fix import FixStringsTools

class Test:

    @pytest.mark.parametrize(("string", "expected"), [
        ("hello_world_ū", "hello_world_uu"),
        ("échos", "echos"),
        #("ñoño", "nono"),
    ])
    def test_fix_string_for_path(self, string, expected):
        assert FixStringsTools.fix_string_for_path(string) == expected
