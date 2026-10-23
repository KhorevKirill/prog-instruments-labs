"""Исключения криптосистемы с готовыми сообщениями для пользователя."""


class MissingFileError(FileNotFoundError):
    """Файл, который нужно прочитать, не существует."""

    def __init__(self, file_path: str) -> None:
        """
        Формирует сообщение об отсутствующем файле.

        :param file_path: путь к файлу
        """
        super().__init__(f"Файл не найден: {file_path}")


class FileWriteError(OSError):
    """Не удалось записать файл."""

    def __init__(self, file_path: str) -> None:
        """
        Формирует сообщение об ошибке записи.

        :param file_path: путь к файлу
        """
        super().__init__(f"Ошибка записи файла: {file_path}")


class JsonFormatError(ValueError):
    """Файл настроек не является корректным JSON."""

    def __init__(self, file_path: str) -> None:
        """
        Формирует сообщение об ошибке разбора JSON.

        :param file_path: путь к JSON-файлу
        """
        super().__init__(f"Ошибка чтения JSON-файла: {file_path}")


class KeySizeError(ValueError):
    """Недопустимая длина ключа 3DES."""

    def __init__(self, key_size: int) -> None:
        """
        Формирует сообщение о неверной длине ключа.

        :param key_size: запрошенная длина ключа в битах
        """
        super().__init__(
            f"Длина ключа 3DES должна быть 64, 128 или 192 бит, "
            f"получено: {key_size}."
        )


class PrivateKeyError(ValueError):
    """Закрытый RSA-ключ не удалось прочитать."""

    def __init__(self) -> None:
        """Формирует сообщение об ошибке чтения ключа."""
        super().__init__("Не удалось прочитать закрытый RSA-ключ.")


class SettingsError(ValueError):
    """Файл настроек не содержит нужных полей."""

    def __init__(self, file_path: str, reason: str) -> None:
        """
        Формирует сообщение о некорректных настройках.

        :param file_path: путь к файлу настроек
        :param reason: что именно не так
        """
        super().__init__(f"Некорректный файл настроек {file_path}: {reason}")
