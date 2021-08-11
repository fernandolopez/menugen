import re
from pathlib import Path
from typing import List

from menugen.menuentry import MenuEntry

from .generichandlers import ExecutableApplication
from .handler import Handler, Priority


class DirectoryWithApplications(Handler, priority=Priority.COMMON_PATTERNS):
    def handle(self, file_path: Path) -> List[MenuEntry]:
        menu_entries = []
        if file_path.is_dir():
            for dentry in file_path.iterdir():
                menu_entries.extend(ExecutableApplication().handle(dentry))

            if menu_entries:
                return menu_entries
            bin_dir = file_path / "bin"
            if bin_dir.is_dir():
                return self.handle(bin_dir)
        return []


class DirectoryWithEquallyNamedExecutableInside(
    Handler, priority=Priority.COMMON_PATTERNS - 10
):
    @staticmethod
    def stem(name: str) -> str:
        try:
            first = re.split(r"\.|-|_| ", name)[0]
        except IndexError:
            return name.lower()
        return first.lower()

    def handle(self, file_path: Path) -> List[MenuEntry]:
        if file_path.is_dir():
            dirname = self.stem(file_path.name)
            apps = [
                path
                for path in file_path.iterdir()
                if path.is_file()
                and path.stat().st_mode & 0o111
                and self.stem(path.name) == dirname
            ]
            if apps:
                return [MenuEntry(dirname.capitalize(), str(apps[0]))]
        return []
