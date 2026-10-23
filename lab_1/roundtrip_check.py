"""
Сквозная проверка программы: генерация ключей, шифрование, дешифрование.

Запускает main.py в отдельном процессе во временном каталоге и сверяет
расшифрованный файл с исходным. Используется командой `make smoke`.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent
MAIN = LAB_DIR / "main.py"
INPUT = LAB_DIR / "input.txt"


def run_mode(flag: str, workdir: Path) -> None:
    """
    Запускает один режим программы.

    :param flag: ключ режима: --gen, --enc или --dec
    :param workdir: каталог с файлом настроек и данными
    """
    # На вопросы о путях к ключам отвечаем Enter: берутся значения из конфига.
    subprocess.run(  # noqa: S603 - запускается наш же скрипт, ввод не внешний
        [sys.executable, str(MAIN), flag, "config.json"],
        cwd=workdir,
        input="\n\n\n",
        text=True,
        check=True,
        capture_output=True,
    )


def main() -> None:
    """Выполняет полный цикл и завершает процесс с кодом 1 при ошибке."""
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        shutil.copy(INPUT, workdir / "input.txt")
        settings = json.loads((LAB_DIR / "config.json").read_text("utf-8"))
        (workdir / "config.json").write_text(json.dumps(settings), "utf-8")

        for flag in ("--gen", "--enc", "--dec"):
            run_mode(flag, workdir)

        original = INPUT.read_bytes()
        decrypted = (workdir / "decrypted.txt").read_bytes()
        encrypted = (workdir / "encrypted.bin").read_bytes()

    if decrypted != original or original in encrypted:
        print("Сквозная проверка не пройдена")
        raise SystemExit(1)
    print("Сквозная проверка пройдена: файл расшифрован без потерь")


if __name__ == "__main__":
    main()
