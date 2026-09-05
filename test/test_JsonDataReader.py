# -*- coding: utf-8 -*-
import json
import pytest

from src.Types import DataType
from src.JsonDataReader import JsonDataReader


class TestJsonDataReader:

    @pytest.fixture()
    def json_content(self) -> tuple[str, DataType]:
        data = {
            "Иванов Иван Иванович": [
                ["математика", 80],
                ["литература", 76]
            ],
            "Петров Петр Петрович": [
                ["математика", 100],
                ["химия", 61]
            ]
        }

        expected: DataType = {
            "Иванов Иван Иванович": [
                ("математика", 80),
                ("литература", 76)
            ],
            "Петров Петр Петрович": [
                ("математика", 100),
                ("химия", 61)
            ]
        }

        return json.dumps(data, ensure_ascii=False), expected

    @pytest.fixture()
    def filepath_and_data(self, json_content, tmpdir):
        json_text, expected = json_content
        p = tmpdir.mkdir("datadir").join("students.json")
        p.write_text(json_text, encoding="utf-8")
        return str(p), expected

    def test_read(self, filepath_and_data):
        filepath, expected = filepath_and_data
        reader = JsonDataReader()
        result = reader.read(filepath)
        assert result == expected
