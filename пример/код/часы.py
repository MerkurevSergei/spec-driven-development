"""Источник времени: в тестах тестовая обвязка подменяет `сейчас`."""
from datetime import datetime


def сейчас() -> datetime:
    return datetime.now()
