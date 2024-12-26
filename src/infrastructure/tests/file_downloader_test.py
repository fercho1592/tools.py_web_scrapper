import pytest
import os
from ..file_manager import FileManager


class Test:
    @staticmethod
    def get_default() -> FileManager:
        return FileManager("./")

    def test_write_file_has_valid_path_then_write_file(self):
        file_path = "./test_file.txt"
        lines = [
            "Test File"
        ]
        Test.get_default().write_file(file_path, lines)
        file_lines =[]
        with open(file_path, "r", encoding="utf-8") as file:
            file_lines = [line.replace("\n","") for line in file.readlines()]
        os.remove(file_path)
        assert lines == file_lines

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
        file_lines = []
        with open(file_path, "r", encoding="utf-8") as file:
            file_lines = [line.replace("\n","") for line in file.readlines()]
        os.remove(file_path)
        lines.extend(lines2)
        assert lines == file_lines
