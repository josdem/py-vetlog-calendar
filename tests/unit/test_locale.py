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

from vetlog_calendar.shared.locale import Locale


def test_return_spanish_title():
    """Test that the title is returned in Spanish"""
    locale = Locale(language="es")
    title = locale.get_event_title(owner="Jose", pet="Sora")
    assert title == "Jose - Cita de vacunación para Sora"


def test_return_english_title():
    """Test that the title is returned in English"""
    locale = Locale()
    title = locale.get_event_title(owner="Jose", pet="Sora")
    assert title == "Jose - Vaccination appointment for Sora"


def test_return_spanish_pet_info():
    """Test that the pet info is returned in Spanish"""
    locale = Locale(language="es")
    pet_info = locale.get_pet_info(pet="Sora")
    assert pet_info == "Cita de vacunación para Sora"


def test_return_english_pet_info():
    """Test that the pet info is returned in English"""
    locale = Locale()
    pet_info = locale.get_pet_info(pet="Sora")
    assert pet_info == "Vaccination appointment for Sora"


def test_return_spanish_location():
    """Test that the location is returned in Spanish"""
    locale = Locale(language="es")
    location = locale.get_event_location()
    assert location == "La que mejor funcione para ambos"


def test_return_english_location():
    """Test that the location is returned in English"""
    locale = Locale()
    location = locale.get_event_location()
    assert location == "Whatever works for you"


def test_return_spanish_thanks():
    """Test that the thanks message is returned in Spanish"""
    locale = Locale(language="es")
    thanks = locale.get_event_thanks()
    assert thanks == "¡Gracias por confiar en Vetlog!"


def test_return_english_thanks():
    """Test that the thanks message is returned in English"""
    locale = Locale()
    thanks = locale.get_event_thanks()
    assert thanks == "Thank you for trusting Vetlog!"


def test_return_spanish_description_note():
    """Test that the description note message is returned in Spanish"""
    locale = Locale(language="es")
    description_note = locale.get_description_note()
    assert description_note == "Nota: Favor de dar seguimiento usando WhatsApp."


def test_return_english_description_note():
    """Test that the description note message is returned in English"""
    locale = Locale()
    description_note = locale.get_description_note()
    assert description_note == "Note: Please follow up by phone."


def test_return_spanish_deworming_title():
    """Test that the deworming title is returned in Spanish"""
    locale = Locale(language="es")
    title = locale.get_deworming_event_title(owner="Jose", pet="Sora")
    assert title == "Jose - Cita de desparasitación para Sora"


def test_return_english_deworming_title():
    """Test that the deworming title is returned in English"""
    locale = Locale()
    title = locale.get_deworming_event_title(owner="Jose", pet="Sora")
    assert title == "Jose - Deworming appointment for Sora"


def test_return_spanish_deworming_description():
    """Test that the deworming description is returned in Spanish"""
    locale = Locale(language="es")
    description = locale.get_deworming_description(pet="Sora", date="2024-01-01")
    assert (
        description
        == "Favor de validar cita de desparasitación para Sora desde que la reciente fue: 2024-01-01\n"
    )


def test_return_english_deworming_description():
    """Test that the deworming description is returned in English"""
    locale = Locale()
    description = locale.get_deworming_description(pet="Sora", date="2024-01-01")
    assert (
        description
        == "Please validate deworming appointment for pet Sora since the last deworming was: 2024-01-01\n"
    )


def test_get_vaccine_type_returns_spanish_translation():
    """Locale translates Rabies to Rabia in Spanish"""
    assert Locale("es").get_vaccine_type("Rabies") == "Dosis: Rabia\n"


def test_get_vaccine_type_returns_name_unchanged_for_english():
    """Locale returns a formatted vaccine type line in English"""
    assert Locale("en").get_vaccine_type("Rabies") == "Vaccine type: Rabies\n"


def test_get_vaccine_type_returns_name_unchanged_for_unknown_in_spanish():
    """Locale returns a formatted vaccine type line in Spanish, even for unknown vaccine names"""
    assert Locale("es").get_vaccine_type("C6CV") == "Dosis: C6CV\n"


def test_get_missing_pet_logs_event_title_spanish():
    """Test that the missing pet logs event title is returned in Spanish"""
    locale = Locale(language="es")
    title = locale.get_missing_pet_logs_event_title()
    assert title == "Médico - Registros médicos pendientes"


def test_get_missing_pet_logs_event_title_english():
    """Test that the missing pet logs event title is returned in English"""
    locale = Locale(language="en")
    title = locale.get_missing_pet_logs_event_title()
    assert title == "Doctor - Missing pet logs"


def test_get_doctor_info_spanish():
    """Test that the doctor info is returned in Spanish"""
    locale = Locale(language="es")
    doctor_info = locale.get_doctor_info()
    assert doctor_info == "Estimad@ Médico,\n"


def test_get_doctor_info_english():
    """Test that the doctor info is returned in English"""
    locale = Locale(language="en")
    doctor_info = locale.get_doctor_info()
    assert doctor_info == "Dear Doctor,\n"


def test_get_pet_logs_info_header_spanish():
    """Test that the pet logs info header is returned in Spanish"""
    locale = Locale(language="es")
    pet_logs_info_header = locale.get_pet_logs_info_header()
    assert (
        pet_logs_info_header
        == "Nuestros registros muestran que no tenemos registros médicos y tuvimos las siguientes cirugías y/o consultas médicas.\n"
    )


def test_get_pet_logs_info_header_english():
    """Test that the pet logs info header is returned in English"""
    locale = Locale(language="en")
    pet_logs_info_header = locale.get_pet_logs_info_header()
    assert (
        pet_logs_info_header
        == "Our records show that we have missing medical logs and we had the following surgeries and/or medical consultations.\n"
    )


def test_get_pet_logs_info_footer_spanish():
    """Test that the pet logs info footer is returned in Spanish"""
    locale = Locale(language="es")
    pet_logs_info_footer = locale.get_pet_logs_info_footer()
    assert (
        pet_logs_info_footer
        == "Favor de crear esos registros médicos en cuanto sea posible.\n"
    )


def test_get_pet_logs_info_footer_english():
    """Test that the pet logs info footer is returned in English"""
    locale = Locale(language="en")
    pet_logs_info_footer = locale.get_pet_logs_info_footer()
    assert (
        pet_logs_info_footer
        == "Please create those medical logs as soon as possible.\n"
    )
