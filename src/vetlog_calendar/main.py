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

import argparse


from .shared.calendar_helper import Helper
from .shared.database import get_session
from .users.repository import UserRepository
from .pets.repository import PetRepository
from .vaccinations.repository import VaccinationRepository, VaccineType
from .vaccinations.service import VaccinationService
from .shared.calendar import Calendar
from .shared.config import Settings
from . import __project__, __version__


def print_paths():
    """Print paths"""
    settings = Settings()
    print(f"Token path: {settings.TOKEN_PATH}")
    print(f"Credentials path: {settings.CREDENTIALS_PATH}")


def list_users():
    """List users with pets with pending vaccinations"""
    with get_session() as session:
        user_repo = UserRepository(session)
        pet_repo = PetRepository(session)
        vaccination_repo = VaccinationRepository(session)
        vaccination_service = VaccinationService(vaccination_repo)

        pending_vaccinations = vaccination_service.get_pending_vaccinations()

        pending_pet_ids = {v.pet_id for v in pending_vaccinations}
        pets = pet_repo.get_all()
        pet_with_pending_vaccinations = [
            pet for pet in pets if pet.id in pending_pet_ids
        ]

        for pet in pet_with_pending_vaccinations:
            owner = (
                user_repo.find_by_id(pet.adopter_id)
                if pet.adopter_id is not None
                else user_repo.find_by_id(pet.user_id)
            )
            print(
                f"{owner.username} - {owner.first_name} {owner.last_name} - {owner.email} - Pet: {pet.name} - awaiting vaccination"
            )


def list_pets():
    """List all owners/adopters with pets waiting for vaccinations"""
    with get_session() as session:
        vaccination_repo = VaccinationRepository(session)
        vaccination_service = VaccinationService(vaccination_repo)
        user_repo = UserRepository(session)
        pet_repo = PetRepository(session)

        pending_vaccinations = vaccination_service.get_pending_vaccinations()

        seen_pets = set()
        for vaccination in pending_vaccinations:
            if vaccination.pet_id not in seen_pets:
                seen_pets.add(vaccination.pet_id)
                pet = pet_repo.find_by_id(vaccination.pet_id)
                owner = (
                    user_repo.find_by_id(pet.adopter_id)
                    if pet.adopter_id is not None
                    else user_repo.find_by_id(pet.user_id)
                )
                print(
                    f"Owner: {owner.first_name} {owner.last_name}, Pet: {pet.name}, awaiting vaccination"
                )


def list_vaccinations(
    calendar: Calendar = None, service: VaccinationService = None, language: str = "en"
):
    """List pending vaccinations"""
    if calendar is None:
        calendar = Calendar()
    with get_session() as session:
        if service is None:
            repo = VaccinationRepository(session)
            service = VaccinationService(repo)

        vaccinations = service.get_pending_vaccinations()

        # If there are no pending vaccinations, print a message and exit
        if not vaccinations:
            print("no new vaccinations were found")
            return

        pet_repository = PetRepository(session)
        user_repository = UserRepository(session)

        for vaccination in vaccinations:
            pet = pet_repository.find_by_id(vaccination.pet_id)

            user = (
                user_repository.find_by_id(pet.adopter_id)
                if pet.adopter_id is not None
                else user_repository.find_by_id(pet.user_id)
            )

            helper = Helper(
                pet=pet, vaccination=vaccination, owner=user, language=language
            )
            event = helper.get_vaccination_event()
            calendar.create_event(event)
            if vaccination.name == VaccineType.RABIES:
                service.delete_rabies_vaccinations_for_pet(pet.id)
            service.update_vaccination_status(vaccination)
            print(event)


def vaccinations_cli():
    """CLI entry point for list_vaccinations"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language",
        type=str.lower,
        choices=["en", "es"],
        default="en",
        help="Language for the calendar events",
    )
    args = parser.parse_args()
    list_vaccinations(language=args.language)


def list_dewormings(
    calendar: Calendar = None, service: VaccinationService = None, language: str = "en"
):
    """List pending dewormings"""
    if calendar is None:
        calendar = Calendar()
    with get_session() as session:
        if service is None:
            repo = VaccinationRepository(session)
            service = VaccinationService(repo)
        user_repo = UserRepository(session)
        pet_repo = PetRepository(session)
        required_dewormings = service.get_pending_dewormings()
        print(f"Found {len(required_dewormings)} pending dewormings")

        for deworming in required_dewormings:
            pet = pet_repo.find_by_id(deworming.pet_id)
            user = (
                user_repo.find_by_id(pet.adopter_id)
                if pet.adopter_id is not None
                else user_repo.find_by_id(pet.user_id)
            )
            helper = Helper(
                pet=pet, vaccination=deworming, owner=user, language=language
            )
            event = helper.get_deworming_event()
            calendar.create_event(event)
            service.update_vaccination_status(deworming)
            print(event)


def dewormings_cli():
    """CLI entry point for list_dewormings"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language",
        type=str.lower,
        choices=["en", "es"],
        default="en",
        help="Language for the calendar events",
    )
    args = parser.parse_args()
    list_dewormings(language=args.language)


def version_check():
    """Print version info"""
    print(f"{__project__} version {__version__}")
