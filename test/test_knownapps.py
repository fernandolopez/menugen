from pathlib import Path
from unittest.mock import patch

from menugen.knownapps import Arduino, FreeCADAppImage, OBSStudioPortable


@patch("menugen.knownapps.Path.is_dir")
@patch("menugen.knownapps.Path.is_file")
def test_arduino_folder_is_detected(mock_is_file, mock_is_dir):
    arduino_app = Arduino().handle(Path("/foo/bar/arduino-1.1.11-r5"))[0]
    assert arduino_app.name == "Arduino 1.1.11 r5"
    assert arduino_app.exec == "/foo/bar/arduino-1.1.11-r5/arduino"


@patch("menugen.knownapps.Path.is_dir")
@patch("menugen.knownapps.Path.is_file")
def test_freecad_appimage_is_detected(mock_is_file, mock_is_dir):
    freecad_path = Path(
        "/foo/bar/FreeCAD_0.18-16146-rev1-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage"
    )
    freecad_app = FreeCADAppImage().handle(freecad_path)[0]
    assert freecad_app.name == "FreeCAD 0.18"
    assert freecad_app.exec == str(freecad_path)


@patch("menugen.knownapps.Path.is_dir")
@patch("menugen.knownapps.Path.is_file")
def test_obs_studio_portable_is_detected(mock_is_file, mock_is_dir):
    obs_path = Path("/foo/bar/obs-studio-portable/")
    obs_app = OBSStudioPortable().handle(obs_path)[0]
    assert obs_app.name == "OBS Studio"
    assert obs_app.exec == str(obs_path / "bin" / "64bit" / "obs")
    assert obs_app.path == obs_path / "bin" / "64bit"
