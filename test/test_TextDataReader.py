# -*- coding: utf-8 -*-
import pytest

from src.Types import DataType
from src.TextDataReader import TextDataReader


class TestTextDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> tuple[str, DataType]:
        text = (
            "Иванов Константин Дмитриевич\n"
            " математика:91\n"
            " химия:100\n"
            "Петров Петр Семенович\n"
            " русский язык:87\n"
            " литература:78\n"
        )

        data: DataType = {
            "Иванов Константин Дмитриевич": [
                ("математика", 91),
                ("химия", 100)
            ],
            "Петров Петр Семенович": [
                ("русский язык", 87),
                ("литература", 78)
            ]
        }

        return text, data

    @pytest.fixture()
    def filepath_and_data(self, file_and_data_content, tmpdir):
        p = tmpdir.mkdir("datadir").join("my_data.txt")
        p.write_text(file_and_data_content[0], encoding='utf-8')
        return str(p), file_and_data_content[1]

    def test_read(self, filepath_and_data) -> None:
        filepath, expected = filepath_and_data
        file_content = TextDataReader().read(filepath)
        assert file_content == expected
