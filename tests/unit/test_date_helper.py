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


from datetime import datetime

from vetlog_calendar.shared.date_helper import validate_date, get_last_deworming_date


def test_move_two_days_if_monday():
    date = datetime(2026, 6, 1)  # Monday
    assert validate_date(date) == datetime(2026, 6, 3)  # Wednesday


def test_move_two_days_if_tuesday():
    date = datetime(2026, 6, 2)  # Tuesday
    assert validate_date(date) == datetime(2026, 6, 4)  # Thursday


def test_no_move_if_wednesday():
    date = datetime(2026, 6, 3)  # Wednesday
    assert validate_date(date) == date


def test_no_move_if_thursday():
    date = datetime(2026, 6, 4)  # Thursday
    assert validate_date(date) == date


def test_no_move_if_friday():
    date = datetime(2026, 6, 5)  # Friday
    assert validate_date(date) == date


def test_no_move_if_saturday():
    date = datetime(2026, 6, 6)  # Saturday
    assert validate_date(date) == date


def test_no_move_if_sunday():
    date = datetime(2026, 6, 7)  # Sunday
    assert validate_date(date) == date


def test_last_deworming_six_months_when_going_out_often():
    assert get_last_deworming_date(datetime(2026, 5, 21), going_out_often=True) == datetime(2025, 11, 21)


def test_last_deworming_one_year_when_not_going_out_often():
    assert get_last_deworming_date(datetime(2026, 5, 21), going_out_often=False) == datetime(2025, 5, 21)


def test_last_deworming_clamps_to_last_day_of_month_when_going_out_often():
    # Aug 31 - 6 months = Feb 28 (not Feb 31 which doesn't exist)
    assert get_last_deworming_date(datetime(2026, 8, 31), going_out_often=True) == datetime(2026, 2, 28)


def test_last_deworming_clamps_leap_year_feb29_when_not_going_out_often():
    # Feb 29 (leap year) - 1 year = Feb 28 (non-leap year)
    assert get_last_deworming_date(datetime(2024, 2, 29), going_out_often=False) == datetime(2023, 2, 28)
