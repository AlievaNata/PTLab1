# -*- coding: utf-8 -*-
import pytest
from src.RatingAnalyzer import RatingAnalyzer


class TestRatingAnalyzer:

    # Проверяет, что при пустом словаре возвращается пустой список.
    def test_empty_ratings(self):
        analyzer = RatingAnalyzer({})
        assert analyzer.get_last_quartile_students() == []

    # Проверяет, что один студент всегда попадает в последнюю квартиль.
    def test_single_student(self):
        analyzer = RatingAnalyzer({"Иванов": 90})
        assert analyzer.get_last_quartile_students() == ["Иванов"]

    # Проверяет, что при одинаковых рейтингах все попадают в квартиль.
    def test_all_equal_ratings(self):
        ratings = {"А": 50, "Б": 50, "В": 50, "Г": 50}
        analyzer = RatingAnalyzer(ratings)
        result = analyzer.get_last_quartile_students()
        assert set(result) == {"А", "Б", "В", "Г"}

    # Проверяет базовый случай: один студент в последней квартиль.
    def test_basic_quartile(self):
        ratings = {"А": 10, "Б": 20, "В": 30, "Г": 40}
        analyzer = RatingAnalyzer(ratings)
        result = analyzer.get_last_quartile_students()
        assert result == ["Г"]

    # Проверяет, что несколько студентов могут попасть в последнюю квартиль.
    def test_multiple_in_last_quartile(self):
        ratings = {"А": 10, "Б": 20, "В": 30, "Г": 40, "Д": 50, "Е": 60}
        analyzer = RatingAnalyzer(ratings)
        result = analyzer.get_last_quartile_students()
        assert set(result) == {"Д", "Е"}

    # Проверяет, что сортировка работает правильно при хаотичном вводе.
    def test_non_sorted_input(self):
        ratings = {"А": 100, "Б": 10, "В": 55, "Г": 80}
        analyzer = RatingAnalyzer(ratings)
        result = analyzer.get_last_quartile_students()
        assert result == ["А"]

    # Проверяет работу с float‑значениями рейтингов.
    def test_float_ratings(self):
        ratings = {"А": 10.5, "Б": 20.2, "В": 30.7, "Г": 40.9}
        analyzer = RatingAnalyzer(ratings)
        result = analyzer.get_last_quartile_students()
        assert result == ["Г"]

    # Проверяет корректный расчёт порога квартиля.
    def test_quartile_threshold(self):
        ratings = {"А": 10, "Б": 20, "В": 30, "Г": 40}
        analyzer = RatingAnalyzer(ratings)
        threshold = analyzer.get_threshold()
        assert threshold == 40

    # Проверяет, что порог сохраняется и используется повторно.
    def test_threshold_saved_and_used(self):
        ratings = {"А": 10, "Б": 20, "В": 30, "Г": 40}
        analyzer = RatingAnalyzer(ratings)

        t1 = analyzer.get_threshold()

        t2 = analyzer.get_threshold()

        assert t1 == t2 == 40

        assert analyzer.get_last_quartile_students() == ["Г"]
