"""Источник времени: в тестах привязка подменяет `сейчас`."""
from datetime import datetime


def сейчас() -> datetime:
    return datetime.now()
