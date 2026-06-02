#  Copyright 2026 Jose Morales contact@josdem.io
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import tomllib
from importlib.metadata import PackageNotFoundError
from pathlib import Path

from vetlog_calendar import __version__, _read_version
from vetlog_calendar.main import version_check


def test_package_version_matches_pyproject():
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    with pyproject_path.open("rb") as pyproject_file:
        expected_version = tomllib.load(pyproject_file)["project"]["version"]

    assert __version__ == expected_version


def test_read_version_falls_back_to_pyproject_when_package_metadata_is_missing(
    monkeypatch,
):
    monkeypatch.setattr(
        "vetlog_calendar.version",
        lambda _: (_ for _ in ()).throw(PackageNotFoundError()),
    )

    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    with pyproject_path.open("rb") as pyproject_file:
        expected_version = tomllib.load(pyproject_file)["project"]["version"]

    assert _read_version() == expected_version


def test_version_check_uses_pyproject_version(caplog):
    caplog.set_level("INFO")
    version_check()

    assert f"vetlog-calendar version {__version__}" in caplog.text
