# -*- coding: utf-8 -*-
from typing import Dict, List


class RatingAnalyzer:
    """Определяет студентов последней квартиль рейтингов."""

    def __init__(self, ratings: Dict[str, float]) -> None:
        self.ratings = ratings
        self.threshold = None  # порог квартиля

    def get_threshold(self) -> float:
        """Возвращает порог последней квартиль."""
        if not self.ratings:
            return None

        values = sorted(self.ratings.values())
        q4_index = int(len(values) * 0.75)
        self.threshold = values[q4_index]
        return self.threshold

    def get_last_quartile_students(self) -> List[str]:
        """Возвращает студентов последней квартиль."""
        if not self.ratings:
            return []

        # если порог ещё не вычислен — вычисляем
        if self.threshold is None:
            self.get_threshold()

        return [
            student
            for student, rating in self.ratings.items()
            if rating >= self.threshold
        ]
