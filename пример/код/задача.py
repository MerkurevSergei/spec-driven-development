from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from код import часы
from код.интеграции.почта import Почта


class СтатусЗадачи(Enum):
    Открыта = "Открыта"
    Закрыта = "Закрыта"


@dataclass
class Задача:
    Название: str
    Адрес: str
    Почта: Почта
    Статус: СтатусЗадачи = СтатусЗадачи.Открыта
    ДатаЗакрытия: datetime | None = None
    Срочная: bool = False
    Приоритет: int = 3

    def Закрыть(self) -> None:
        if self.Статус == СтатусЗадачи.Закрыта:
            raise ValueError("Задача уже закрыта")
        self.Статус = СтатусЗадачи.Закрыта
        self.ДатаЗакрытия = часы.сейчас()

    def Выполнить(self) -> None:
        снимок = (self.Статус, self.ДатаЗакрытия)
        self._Выполнить_шаг1()
        if self.Срочная:
            try:
                self._Выполнить_шаг2()
            except Exception:
                self.Статус, self.ДатаЗакрытия = снимок
                raise

    def _Выполнить_шаг1(self) -> None:
        self.Закрыть()

    def _Выполнить_шаг2(self) -> None:
        self.Почта.Отправить(self.Адрес, "Задача выполнена: " + self.Название)

    def ПовыситьПриоритет(self) -> None:
        if self.Приоритет + 1 > 5:
            raise ValueError("Приоритет уже наивысший")
        self.Приоритет += 1

    def Факториал(self, N: int) -> int:
        if N < 0:
            raise ValueError("Факториал определён для N ≥ 0")
        if N == 0:
            return 1
        return N * self.Факториал(N - 1)
