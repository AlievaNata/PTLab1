# -*- coding: utf-8 -*-
import json
from Types import DataType
from DataReader import DataReader


class JsonDataReader(DataReader):
    """Читает данные студентов из JSON‑файла."""

    def __init__(self) -> None:
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        # Загружаем JSON
        with open(path, encoding="utf-8") as file:
            data = json.load(file)

        # Проверка: JSON должен быть словарём
        if not isinstance(data, dict):
            raise TypeError("Ожидался словарь студентов")

        result: DataType = {}

        for student, subjects in data.items():

            # Проверка: список предметов
            if not isinstance(subjects, list):
                raise TypeError("Ожидался список предметов")

            parsed_subjects = []

            for item in subjects:

                # Каждый предмет должен быть списком из двух элементов
                if not isinstance(item, list) or len(item) != 2:
                    raise TypeError(
                        "Каждый предмет должен быть списком из двух элементов"
                    )
                subj, score = item

                # Проверка типов
                if not isinstance(subj, str):
                    raise TypeError("Название предмета должно быть строкой")

                # Преобразуем оценку в int
                try:
                    score = int(score)
                except (ValueError, TypeError):
                    raise TypeError("Оценка должна быть числом")

                parsed_subjects.append((subj, score))

            result[student] = parsed_subjects

        self.students = result
        return result
