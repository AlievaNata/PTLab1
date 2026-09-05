# -*- coding: utf-8 -*-
import json
from Types import DataType
from DataReader import DataReader


class JsonDataReader(DataReader):
    """Читает данные студентов из JSON‑файла."""

    def __init__(self) -> None:
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)

        # Преобразуем JSON‑структуру в DataType
        for student, subjects in data.items():
            self.students[student] = [
                (subj, int(score)) for subj, score in subjects
            ]

        return self.students
