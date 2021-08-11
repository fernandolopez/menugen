from fnmatch import fnmatch
from pathlib import Path
from typing import List, Union

import magic

from .handler import Handler, Priority
from .menuentry import MenuEntry

EXCLUDE_MIMETYPES = {"application/x-sharedlib"}
EXCLUDE_FILENAME_PATTERNS = [
    "fsnotifier*",
    "format.sh",
    "inspect.sh",
    "profiler.sh",
    "game-tools.sh",
]


class ExecutableApplication(Handler, priority=Priority.GENERIC_APPS):
    def handle(self, file_path: Path) -> List[MenuEntry]:
        if file_path.is_file() and file_path.stat().st_mode & 0o111:
            mime_type = magic.from_file(str(file_path), mime=True)
            if mime_type in EXCLUDE_MIMETYPES:
                return []
            if [
                match
                for match in EXCLUDE_FILENAME_PATTERNS
                if fnmatch(file_path.name, match)
            ]:
                return []
            if (
                mime_type.startswith("application/")
                or mime_type == "text/x-shellscript"
            ):
                return [MenuEntry(file_path.name, str(file_path))]
        return []


class WineApplication(Handler, priority=Priority.GENERIC_APPS):
    def handle(self, file_path: Path) -> List[MenuEntry]:
        if file_path.is_file() and file_path.suffix == ".exe":
            return [MenuEntry(file_path.stem, f"wine {file_path}")]
        return []
