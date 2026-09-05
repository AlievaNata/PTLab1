# -*- coding: utf-8 -*-
import argparse
import sys
import os

from CalcRating import CalcRating
from TextDataReader import TextDataReader
from JsonDataReader import JsonDataReader
from RatingAnalyzer import RatingAnalyzer


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument(
        "-p",
        dest="path",
        type=str,
        required=True,
        help="Path to datafile"
    )
    args = parser.parse_args(args)
    return args.path


def select_reader(path: str):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        return TextDataReader()
    elif ext == ".json":
        return JsonDataReader()
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def main():
    path = get_path_from_arguments(sys.argv[1:])
    reader = select_reader(path)

    students = reader.read(path)
    print("Students:", students)

    rating = CalcRating(students).calc()
    print("Rating:", rating)

    analyzer = RatingAnalyzer(rating)
    threshold = analyzer.get_threshold()
    last_quartile = analyzer.get_last_quartile_students()

    print("\nПоследняя квартиль студентов")
    print(f"Порог квартиля (Q4): {threshold}")

    for student in last_quartile:
        print(f"{student}: {rating[student]}")


if __name__ == "__main__":
    main()
