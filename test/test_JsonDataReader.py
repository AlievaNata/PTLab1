# -*- coding: utf-8 -*-
import json
import pytest

from src.JsonDataReader import JsonDataReader
from src.Types import DataType


class TestJsonDataReader:

    # ---------- Позитивный тест: корректный JSON ----------
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

    def test_read_valid_json(self, filepath_and_data):
        filepath, expected = filepath_and_data
        reader = JsonDataReader()
        result = reader.read(filepath)
        assert result == expected

    # ---------- Ошибка: файл не существует ----------
    def test_read_file_not_exists(self):
        reader = JsonDataReader()
        with pytest.raises(FileNotFoundError):
            reader.read("no_such_file.json")

    # ---------- Ошибка: JSON повреждён ----------
    def test_read_invalid_json(self, tmpdir):
        p = tmpdir.mkdir("datadir").join("bad.json")
        p.write_text("{ invalid json", encoding="utf-8")

        reader = JsonDataReader()
        with pytest.raises(json.JSONDecodeError):
            reader.read(str(p))

    # ---------- Ошибка: JSON пустой ----------
    def test_read_empty_file(self, tmpdir):
        p = tmpdir.mkdir("datadir").join("empty.json")
        p.write_text("", encoding="utf-8")

        reader = JsonDataReader()
        with pytest.raises(json.JSONDecodeError):
            reader.read(str(p))

    # ---------- Ошибка: неправильная структура JSON ----------
    def test_read_wrong_structure(self, tmpdir):
        p = tmpdir.mkdir("datadir").join("wrong.json")
        p.write_text('{"Иванов": "математика"}', encoding="utf-8")

        reader = JsonDataReader()
        with pytest.raises(TypeError):
            reader.read(str(p))

    # ---------- Пустой список предметов ----------
    def test_read_empty_subjects(self, tmpdir):
        p = tmpdir.mkdir("datadir").join("empty_subjects.json")
        p.write_text('{"Иванов": []}', encoding="utf-8")

        reader = JsonDataReader()
        result = reader.read(str(p))
        assert result == {"Иванов": []}

    # ---------- Оценки строками ----------
    def test_read_scores_as_strings(self, tmpdir):
        p = tmpdir.mkdir("datadir").join("scores.json")
        p.write_text('{"Иванов": [["математика", "80"]]}', encoding="utf-8")

        reader = JsonDataReader()
        result = reader.read(str(p))
        assert result == {"Иванов": [("математика", 80)]}

    # ---------- Оценки float ----------
    def test_read_scores_float(self, tmpdir):
        p = tmpdir.mkdir("datadir").join("float.json")
        p.write_text('{"Иванов": [["математика", 80.5]]}', encoding="utf-8")

        reader = JsonDataReader()
        result = reader.read(str(p))
        assert result == {"Иванов": [("математика", 80)]}

    # ---------- Несколько студентов ----------
    def test_read_multiple_students(self, tmpdir):
        p = tmpdir.mkdir("datadir").join("multi.json")
        p.write_text(
            json.dumps({
                "А": [["математика", 1]],
                "Б": [["химия", 2]],
                "В": [["физика", 3]]
            }, ensure_ascii=False),
            encoding="utf-8"
        )

        reader = JsonDataReader()
        result = reader.read(str(p))

        assert result == {
            "А": [("математика", 1)],
            "Б": [("химия", 2)],
            "В": [("физика", 3)]
        }
        