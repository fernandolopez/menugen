from pathlib import Path

from menugen.menuentry import MenuEntry


def test_menu_entry_exports_to_xdg_desktop_format():
    mentry = MenuEntry(
        "App",
        "/app/run",
        path=Path("/app/working_dir"),
        description="This is an app",
        icon="/app/icon.png",
    )
    desktop_file_data = mentry.export().split("\n")
    assert "Name=App" in desktop_file_data
    assert "Exec=/app/run" in desktop_file_data
    assert "Path=/app/working_dir" in desktop_file_data
    assert "Description=This is an app" in desktop_file_data
    assert "Icon=/app/icon.png" in desktop_file_data
