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

    def test_write_file_has_existent_file_then_write_file(self):
        file_path = "./test_file.txt"
        lines = [
            "Test File",
            "test Line"
        ]
        lines2 = [
            "Test File2"
        ]
        Test.get_default().write_file(file_path, lines)
        Test.get_default().write_file(file_path, lines2)
        with open(file_path, "r", encoding="utf-8") as file:
            file_lines = file.readlines()
            assert lines.extend(lines2) == file_lines
        os.remove(file_path)
