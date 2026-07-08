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

from vetlog_calendar.shared.medical_helper import is_medical_event


def test_is_surgery_detects_english_surgery():
    """Detect surgery events in English"""
    assert is_medical_event("Jose - Surgery appointment for Sora")


def test_is_surgery_detects_spanish_cirugia():
    """Detect surgery events in Spanish without accent"""
    assert is_medical_event("Jose - Cirugia appointment for Sora")


def test_is_surgery_detects_spanish_cirugia_with_accent():
    """Detect surgery events in Spanish with accent"""
    assert is_medical_event("Jose - Cirugía appointment for Sora")


def test_is_surgery_ignores_non_surgery_event():
    """Ignore events that are not surgeries"""
    assert not is_medical_event("Jose - Vaccination appointment for Sora")


def test_is_surgery_detects_spay_surgery():
    """Detect Spay surgery events in English"""
    assert is_medical_event("Jose - Spay surgery appointment for Sora")


def test_is_surgery_detects_neuer_surgery():
    """Detect Neuer surgery events in English"""
    assert is_medical_event("Jose - Neuer surgery appointment for Nico")


def test_is_surgery_detects_medical_appointment():
    """Detect medical appointment events in English"""
    assert is_medical_event("Jose - Medical appointment for Sora")


def test_is_surgery_detects_medical_appointment_in_spanish():
    """Detect medical appointment events in Spanish"""
    assert is_medical_event("Jose - Cita médica para Sora")


def test_is_surgery_detects_medical_appointment_in_spanish_without_accent():
    """Detect medical appointment events in Spanish"""
    assert is_medical_event("Jose - Cita medica para Sora")


def test_is_surgery_detects_special_spanish_surgery_keyword_in_spanish():
    """Detect special surgery keyword in appointment events in Spanish"""
    assert is_medical_event("Jose - Cita esterilización para Sora")


def test_is_surgery_detects_special_spanish_surgery_keyword_in_spanish_without_accent():
    """Detect special surgery keyword in appointment events in Spanish without accent"""
    assert is_medical_event("Jose - Cita esterilizacion para Sora")


def test_should_not_detect_as_medical_event_if_keyword_is_medicamento():
    """Should not detect as medical event if the keyword is 'medicamento'"""
    assert not is_medical_event("Sonia - Cita shot de medicamento para Deimos")
