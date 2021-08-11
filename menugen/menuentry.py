from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class MenuEntry:
    name: str
    exec: str
    path: Optional[Path] = None
    description: Optional[str] = None
    icon: Optional[str] = None

    def export(self) -> str:
        dentry = [
            "[Desktop Entry]",
            "Version=1.0",
            "Type=Application",
            f"Name={self.name}",
            f"Exec={self.exec}",
        ]
        if self.path is not None:
            dentry.append(f"Path={self.path}")
        if self.description is not None:
            dentry.append(f"Description={self.description}")
        if self.icon is not None:
            dentry.append(f"Icon={self.icon}")

        return "\n".join(dentry)
