"""Типизированные настройки криптосистемы и их проверка."""

from typing import TypedDict, cast

from errors import SettingsError

PATH_FIELDS = (
    "input_file",
    "encrypted_file",
    "decrypted_file",
    "symmetric_key",
    "public_key",
    "private_key",
)


class Settings(TypedDict):
    """Содержимое файла настроек config.json."""

    key_size: int
    input_file: str
    encrypted_file: str
    decrypted_file: str
    symmetric_key: str
    public_key: str
    private_key: str


def parse_settings(data: object, source: str) -> Settings:
    """
    Проверяет данные, прочитанные из JSON, и превращает их в Settings.

    :param data: результат json.load
    :param source: путь к файлу настроек, для сообщения об ошибке
    :return: проверенные настройки
    """
    if not isinstance(data, dict):
        raise SettingsError(source, "ожидается JSON-объект")
    raw = cast("dict[str, object]", data)

    key_size = raw.get("key_size")
    if not isinstance(key_size, int) or isinstance(key_size, bool):
        raise SettingsError(source, "поле key_size должно быть числом")

    paths: dict[str, str] = {}
    for field in PATH_FIELDS:
        value = raw.get(field)
        if not isinstance(value, str):
            raise SettingsError(source, f"поле {field} должно быть строкой")
        paths[field] = value

    return Settings(
        key_size=key_size,
        input_file=paths["input_file"],
        encrypted_file=paths["encrypted_file"],
        decrypted_file=paths["decrypted_file"],
        symmetric_key=paths["symmetric_key"],
        public_key=paths["public_key"],
        private_key=paths["private_key"],
    )
