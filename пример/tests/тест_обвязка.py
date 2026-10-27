"""Тестовая обвязка спецификации и кода: единственный тестовый код, который пишется руками (или ИИ).

Тестовая обвязка только создаёт объекты и читает их; ожидания живут в сгенерированных тестах.
"""
from contextlib import contextmanager
from dataclasses import fields, is_dataclass
from datetime import datetime
from enum import Enum
from typing import get_type_hints

from код import задача, почта, часы

МОДУЛИ = [задача, почта]


class Сбой(Exception):
    """Искусственный сбой шага."""


class Регистратор:
    """Замена внешнего объекта: запоминает вызовы, ничего не делает."""

    def __init__(self, Объект: str):
        self.Объект = Объект
        self.вызовы = []

    def __getattr__(self, метод):
        def вызов(*аргументы):
            self.вызовы.append((метод, аргументы))
        return вызов


def класс(Объект: str):
    for модуль in МОДУЛИ:
        if hasattr(модуль, Объект):
            return getattr(модуль, Объект)
    return None


def внешний(Объект: str) -> Регистратор:
    return Регистратор(Объект)


def создать(Объект: str, значения: dict):
    cls = класс(Объект)
    типы = get_type_hints(cls)
    аргументы = {}
    for имя, значение in значения.items():
        тип = типы.get(имя)
        if isinstance(тип, type) and issubclass(тип, Enum) and isinstance(значение, str):
            значение = тип[значение]
        аргументы[имя] = значение
    return cls(**аргументы)


def прочитать(объект) -> dict:
    результат = {}
    for поле in fields(объект):
        значение = getattr(объект, поле.name)
        if isinstance(значение, Регистратор):
            continue
        if isinstance(значение, Enum):
            значение = значение.name
        elif is_dataclass(значение):
            значение = прочитать(значение)
        результат[поле.name] = значение
    return результат


def сейчас(момент: datetime) -> None:
    часы.сейчас = lambda: момент


@contextmanager
def сбой_на_шаге(Объект: str, Метод: str, N: int):
    cls = класс(Объект)
    имя = f"_{Метод}_шаг{N}"
    прежний = getattr(cls, имя)

    def сбой(self):
        raise Сбой(f"{Объект}.{Метод}: шаг {N}")

    setattr(cls, имя, сбой)
    try:
        yield
    finally:
        setattr(cls, имя, прежний)


def значения_перечисления(Имя: str) -> list[str]:
    return [з.name for з in класс(Имя)]
