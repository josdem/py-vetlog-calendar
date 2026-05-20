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

import calendar
from datetime import datetime, timedelta


def validate_date(date: datetime) -> datetime:
    """Validate if day of the week is valid"""
    match date.weekday():
        case 0 | 1:
            return date + timedelta(days=2)
        case _:
            return date


def get_last_deworming_date(vaccination_date: datetime, going_out_often: bool) -> datetime:
    """Return estimated last deworming date: 6 months before appointment if pet goes out often, else 1 year before"""
    if going_out_often:
        month = vaccination_date.month - 6
        year = vaccination_date.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
    else:
        year = vaccination_date.year - 1
        month = vaccination_date.month
    day = min(vaccination_date.day, calendar.monthrange(year, month)[1])
    return vaccination_date.replace(year=year, month=month, day=day)
