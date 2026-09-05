# -*- coding: utf-8 -*-
import pytest

from src.main import get_path_from_arguments


@pytest.fixture()
def correct_arguments_string() -> tuple[list[str], str]:
    return ["-p", "/home/user/file.txt"], "/home/user/file.txt"


@pytest.fixture()
def noncorrect_arguments_string() -> list[str]:
    return ["/home/user/file.txt"]


def test_get_path_from_correct_arguments(correct_arguments_string) -> None:
    args, expected = correct_arguments_string
    path = get_path_from_arguments(args)
    assert path == expected


def test_get_path_from_noncorrect_arguments(
    noncorrect_arguments_string
) -> None:
    with pytest.raises(SystemExit):
        get_path_from_arguments(noncorrect_arguments_string)
