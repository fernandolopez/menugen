#!/usr/bin/env python3

import shutil
from pathlib import Path

from .commonpatterns import *
from .generichandlers import *
from .handler import Handler
from .knownapps import *

home = Path.home()
menu_path = home / ".local/share/applications/menugen"


apps_paths = [home / "opt"]

handlers = [
    handler()
    for _, handler_set in sorted(Handler.handlers.items(), key=lambda item: item[0])
    for handler in handler_set
]


def main():
    menus = []

    for apps_path in apps_paths:
        for subdir in apps_path.iterdir():
            print(subdir)
            for handler in handlers:
                menu = handler.handle(subdir)
                if menu:
                    menus.extend(menu)
                    break

    shutil.rmtree(menu_path)
    menu_path.mkdir(parents=True, exist_ok=True)
    for menu in menus:
        with open(menu_path / f"{menu.name}.desktop", "w") as f:
            f.write(menu.export())


if __name__ == "__main__":
    main()
