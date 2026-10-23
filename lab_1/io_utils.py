"""Чтение и запись JSON-настроек и бинарных файлов."""

import json
from collections.abc import Mapping
from pathlib import Path

from errors import FileWriteError, JsonFormatError, MissingFileError


def load_json(file_path: str) -> object:
    """
    Читает JSON-файл.

    :param file_path: путь к JSON-файлу
    :return: данные из JSON-файла
    """
    try:
        with Path(file_path).open(encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise MissingFileError(file_path) from error
    except json.JSONDecodeError as error:
        raise JsonFormatError(file_path) from error


def dump_json(file_path: str, data: Mapping[str, object]) -> None:
    """
    Записывает словарь в JSON-файл.

    :param file_path: путь к JSON-файлу
    :param data: данные для записи
    :return: None
    """
    try:
        with Path(file_path).open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except OSError as error:
        raise FileWriteError(file_path) from error


def load_blob(file_path: str) -> bytes:
    """
    Читает бинарный файл.

    :param file_path: путь к файлу
    :return: данные из файла
    """
    try:
        with Path(file_path).open("rb") as file:
            return file.read()
    except FileNotFoundError as error:
        raise MissingFileError(file_path) from error


def dump_blob(file_path: str, data: bytes) -> None:
    """
    Записывает данные в бинарный файл.

    :param file_path: путь к файлу
    :param data: данные для записи
    :return: None
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with Path(file_path).open("wb") as file:
            file.write(data)
    except OSError as error:
        raise FileWriteError(file_path) from error
