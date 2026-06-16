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

import os
from pydantic_core import ValidationError
import pytest
from unittest.mock import patch
from vetlog_calendar.shared.config import Settings


@pytest.fixture
def mock_env_vars():
    with patch.dict(
        os.environ,
        {
            "DB_HOST": "localhost",
            "DB_NAME": "vetlog",
            "DB_USER": "vetlogUser",
            "DB_PASSWORD": "vetlogDB",
            "TOKEN_PATH": "token_path_value/token.json",
            "CREDENTIALS_PATH": "token_path_value/credentials.json",
            "DEFAULT_EMAILS": '["email1@example.com", "email2@example.com", "email3@example.com"]',
            "DOCTOR_INFO": "Dear Doctor,",
            "DOCTOR_INFO_ES": "Estimad@ Médico,",
        },
    ):
        yield


@pytest.fixture
def clean_env():
    with patch.dict(os.environ, {}, clear=True):
        yield


def test_settings_loads_from_env(mock_env_vars):
    settings = Settings()
    assert settings.db_host == "localhost"
    assert settings.db_name == "vetlog"
    assert settings.db_user == "vetlogUser"
    assert settings.db_password == "vetlogDB"
    assert settings.TOKEN_PATH == "token_path_value/token.json"
    assert settings.CREDENTIALS_PATH == "token_path_value/credentials.json"
    assert settings.DEFAULT_EMAILS == [
        "email1@example.com",
        "email2@example.com",
        "email3@example.com",
    ]


def test_settings_missing_required_vars(clean_env):
    with pytest.raises(ValidationError):
        Settings(_env_file=None)
