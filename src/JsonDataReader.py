# -*- coding: utf-8 -*-
import json
from Types import DataType
from DataReader import DataReader


class JsonDataReader(DataReader):
    """Читает данные студентов из JSON‑файла с предметами в виде словаря."""

    def __init__(self) -> None:
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        # Загружаем JSON
        with open(path, encoding="utf-8") as file:
            data = json.load(file)

        # Проверка: JSON должен быть словарём студентов
        if not isinstance(data, dict):
            raise TypeError("Ожидался словарь студентов")

        result: DataType = {}

        for student, subjects in data.items():
            # Проверка: предметы должны быть словарём
            if not isinstance(subjects, dict):
                raise TypeError("Ожидался словарь предметов")

            parsed_subjects = []
            for subj, score in subjects.items():
                if not isinstance(subj, str):
                    raise TypeError("Название предмета должно быть строкой")

                try:
                    score = int(score)
                except (ValueError, TypeError):
                    raise TypeError("Оценка должна быть числом")

                parsed_subjects.append((subj, score))

            result[student] = parsed_subjects

        self.students = result
        return result
