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

import logging

from vetlog_calendar.shared.logger import Logger


def test_logger_uses_datetime_level_and_message_format():
    logger = Logger("vetlog_calendar.tests.logger")

    assert logger.log.level == logging.INFO
    assert logger.console_handler.formatter._fmt == (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def test_logger_info_logs_message(caplog):
    logger = Logger("vetlog_calendar.tests.logger_info")
    caplog.set_level("INFO")

    logger.info("Processed %s events", 3)

    assert "Processed 3 events" in caplog.text
