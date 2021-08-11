from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from menugen.commonpatterns import (
    DirectoryWithApplications,
    DirectoryWithEquallyNamedExecutableInside,
)


def test_directory_with_applications():
    with TemporaryDirectory() as tdir:
        tdir = Path(tdir)
        applications = []
        for i in range(2):
            applications.append(tdir / f"baz_{i}.sh")
            with open(applications[-1], "w") as f:
                f.write("#!/bin/sh\ntrue\n")
            applications[-1].chmod(0o755)

        dwa = DirectoryWithApplications().handle(tdir)
        dwa.sort(key=lambda me: me.name)
        assert dwa[0].name == "baz_0.sh"
        assert dwa[0].exec == str(applications[0])
        assert dwa[1].name == "baz_1.sh"
        assert dwa[1].exec == str(applications[1])


def test_directory_with_applications_with_bin_subdirectory():
    with TemporaryDirectory() as tdir:
        tdir = Path(tdir)
        application_dir = tdir / "bin"
        application_dir.mkdir()
        applications = []
        for i in range(2):
            applications.append(application_dir / f"baz_{i}.sh")
            with open(applications[-1], "w") as f:
                f.write("#!/bin/sh\ntrue\n")
            applications[-1].chmod(0o755)

        dwa = DirectoryWithApplications().handle(tdir)
        dwa.sort(key=lambda me: me.name)
        assert dwa[0].name == "baz_0.sh"
        assert dwa[0].exec == str(applications[0])
        assert dwa[1].name == "baz_1.sh"
        assert dwa[1].exec == str(applications[1])


@pytest.mark.parametrize(
    "appname,dirname,filename",
    [
        ("Discord", "Discord", "Discord"),
        ("Firefox", "firefox", "firefox-bin"),
        ("Processing", "processing-3.3.5", "processing"),
    ],
)
def test_directory_equally_named_executable_inside(appname, dirname, filename):
    with TemporaryDirectory() as tdir:
        tdir = Path(tdir)
        application_dir = tdir / dirname
        application = application_dir / filename
        application_dir.mkdir()
        with open(application, "w") as f:
            f.write("#!/bin/sh\ntrue\n")
        application.chmod(0o755)

        dwenei = DirectoryWithEquallyNamedExecutableInside().handle(application_dir)[0]
        assert dwenei.name == appname
        assert dwenei.exec == str(application)
