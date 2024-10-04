import pytest
import os
from ..file_manager import FileDownloader


class Test:
    @staticmethod
    def get_default() -> FileDownloader:
        return FileDownloader("./")

    def test_write_file_has_valid_path_then_write_file(self):
        file_path = "./test_file.txt"
        lines = [
            "Test File"
        ]
        Test.get_default().write_file(file_path, lines)
        with open(file_path, "r", encoding="utf-8") as file:
            assert lines == file.readlines()
        os.remove(file_path)
