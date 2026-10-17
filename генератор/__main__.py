"""python -m генератор <папка спецификаций> <файл тестов>"""
import sys
from pathlib import Path

from .генерация import Генератор
from .парсер import ОшибкаСпецификации, прочитать_спецификации


def главная(аргументы: list[str]) -> int:
    if len(аргументы) != 2:
        print("использование: python -m генератор <папка спецификаций> <файл тестов>", file=sys.stderr)
        return 2
    папка, файл = Path(аргументы[0]), Path(аргументы[1])
    try:
        объекты = прочитать_спецификации(папка)
        текст = Генератор(объекты).все()
    except ОшибкаСпецификации as ошибка:
        print(f"спецификация: {ошибка}", file=sys.stderr)
        return 1
    файл.write_text(текст + "\n", encoding="utf-8")
    print(f"{файл}: {текст.count('    def test_')} тестов")
    return 0


if __name__ == "__main__":
    sys.exit(главная(sys.argv[1:]))
