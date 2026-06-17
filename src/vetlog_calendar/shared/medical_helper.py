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

KEYWORDS = [
    "spay",
    "neuter",
    "medical",
    "surgery",
    "cirugia",
    "cirugía",
    "esterilización",
    "esterilizacion",
    "médica",
    "medica",
]


def is_medical_event(title: str) -> bool:
    """Determines if an event is a medical event based on its title."""
    title = title.lower()
    return any(keyword in title for keyword in KEYWORDS)
