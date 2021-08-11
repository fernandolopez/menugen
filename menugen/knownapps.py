import re
from pathlib import Path
from typing import List

from menugen.menuentry import MenuEntry

from .handler import Handler, Priority


class Arduino(Handler, priority=Priority.KNOWN_APPS):
    def handle(self, file_path: Path) -> List[MenuEntry]:
        if file_path.is_dir():
            name, *version = file_path.name.split("-")
            version = " ".join(version)
            script = file_path / "arduino"
            if name == "arduino" and script.is_file():
                return [MenuEntry(f"Arduino {version}", str(script))]
        return []


class FreeCADAppImage(Handler, priority=Priority.KNOWN_APPS):
    def handle(self, file_path: Path) -> List[MenuEntry]:
        if (
            file_path.is_file()
            and file_path.name.startswith("FreeCAD")
            and file_path.suffix == ".AppImage"
        ):
            parts = re.split("-|_", file_path.stem)
            if len(parts) < 2:
                return []
            return [MenuEntry(f"FreeCAD {parts[1]}", str(file_path))]
        return []


class OBSStudioPortable(Handler, priority=Priority.KNOWN_APPS):
    def handle(self, file_path: Path) -> List[MenuEntry]:
        executable = file_path / "bin" / "64bit" / "obs"

        if (
            file_path.is_dir()
            and file_path.name == "obs-studio-portable"
            and executable.is_file()
        ):
            return [MenuEntry(f"OBS Studio", str(executable), path=executable.parent)]
        return []
