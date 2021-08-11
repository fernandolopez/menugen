from pathlib import Path
from unittest.mock import patch

import magic

from menugen.generichandlers import ExecutableApplication, WineApplication
from menugen.menuentry import MenuEntry


@patch("menugen.generichandlers.Path.stat")
@patch("menugen.generichandlers.Path.is_file")
@patch("menugen.generichandlers.magic.from_file")
def test_executable_files_with_application_mimetype_are_accepted(
    mock_magic_from_file, mock_is_file, mock_stat
):
    mock_magic_from_file.return_value = "application/something"
    mock_is_file.return_value = True
    mock_stat.return_value.st_mode = 0o111
    ea = ExecutableApplication()
    assert isinstance(ea.handle(Path("/foo/bar"))[0], MenuEntry)


@patch("menugen.generichandlers.Path.stat")
@patch("menugen.generichandlers.Path.is_file")
@patch("menugen.generichandlers.magic.from_file")
def test_executable_files_with_x_shellscript_mimetype_are_accepted(
    mock_magic_from_file, mock_is_file, mock_stat
):
    mock_magic_from_file.return_value = "text/x-shellscript"
    mock_is_file.return_value = True
    mock_stat.return_value.st_mode = 0o111
    ea = ExecutableApplication()
    assert isinstance(ea.handle(Path("/foo/bar"))[0], MenuEntry)


@patch("menugen.generichandlers.Path.stat")
@patch("menugen.generichandlers.Path.is_file")
@patch("menugen.generichandlers.magic.from_file")
def test_non_executable_files_with_application_mimetype_are_rejected(
    mock_magic_from_file, mock_is_file, mock_stat
):
    mock_magic_from_file.return_value = "application/something"
    mock_is_file.return_value = True
    mock_stat.return_value.st_mode = 0o444
    ea = ExecutableApplication()
    assert ea.handle(Path("/foo/bar")) == []


@patch("menugen.generichandlers.Path.stat")
@patch("menugen.generichandlers.Path.is_file")
@patch("menugen.generichandlers.magic.from_file")
def test_executable_shared_libraries_rejected(
    mock_magic_from_file, mock_is_file, mock_stat
):
    mock_magic_from_file.return_value = "application/x-sharedlib"
    mock_is_file.return_value = True
    mock_stat.return_value.st_mode = 0o555
    ea = ExecutableApplication()
    assert ea.handle(Path("/foo/bar")) == []


@patch("menugen.generichandlers.Path.stat")
@patch("menugen.generichandlers.Path.is_file")
@patch("menugen.generichandlers.magic.from_file")
def test_executable_files_with_other_mimetypes_are_rejected(
    mock_magic_from_file, mock_is_file, mock_stat
):
    mock_magic_from_file.return_value = "image/png"
    mock_is_file.return_value = True
    mock_stat.return_value.st_mode = 0o777
    ea = ExecutableApplication()
    assert ea.handle(Path("/foo/bar")) == []


@patch("menugen.generichandlers.Path.is_file")
def test_executable_application_ignores_non_files(mock_is_file):
    mock_is_file.return_value = False
    ea = ExecutableApplication()
    assert ea.handle(Path("/foo/bar")) == []


@patch("menugen.generichandlers.Path.stat")
@patch("menugen.generichandlers.Path.is_file")
@patch("menugen.generichandlers.magic.from_file")
def test_executable_application_takes_name_and_exec_from_path(
    mock_magic_from_file, mock_is_file, mock_stat
):
    mock_magic_from_file.return_value = "application/something"
    mock_is_file.return_value = True
    mock_stat.return_value.st_mode = 0o111
    ea = ExecutableApplication()
    bar_menu_entry = ea.handle(Path("/foo/bar"))[0]
    assert bar_menu_entry.name == "bar"
    assert bar_menu_entry.exec == "/foo/bar"


@patch("menugen.generichandlers.Path.is_file")
def test_wine_application_accepts_exe_files(mock_is_file):
    mock_is_file.return_value = True
    wa = WineApplication()
    bar_menu_entry = wa.handle(Path("/foo/bar.exe"))[0]
    assert bar_menu_entry.name == "bar"
    assert bar_menu_entry.exec == "wine /foo/bar.exe"


@patch("menugen.generichandlers.Path.is_file")
def test_wine_application_rejects_non_exe_files(mock_is_file):
    mock_is_file.return_value = True
    wa = WineApplication()
    assert wa.handle(Path("/foo/bar")) == []
