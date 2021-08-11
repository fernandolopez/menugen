from abc import ABC, abstractmethod
from collections import defaultdict
from enum import IntEnum
from pathlib import Path
from typing import List, MutableMapping, Union

from .menuentry import MenuEntry


class Priority(IntEnum):
    KNOWN_APPS: int = 0
    COMMON_PATTERNS: int = 100
    GENERIC_APPS: int = 1000


class Handler(ABC):
    handlers: MutableMapping[int, "Handler"] = defaultdict(list)

    def __init_subclass__(cls, /, priority: Union[Priority, int], **kwargs) -> None:
        Handler.handlers[int(priority)].append(cls)
        return super().__init_subclass__(**kwargs)

    @abstractmethod
    def handle(self, file_path: Path) -> List[MenuEntry]:
        pass
