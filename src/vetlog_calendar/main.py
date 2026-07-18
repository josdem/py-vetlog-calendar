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
from vetlog_calendar.shared import date_helper

from . import __project__, __version__
import argparse


from .shared.calendar_helper import Helper
from .shared.database import get_session
from .users.repository import UserRepository
from .pets.repository import PetRepository
from .vaccinations.repository import VaccinationRepository, VaccineType
from .vaccinations.service import VaccinationService
from .shared.calendar import Calendar
from .shared.identifier_helper import get_vetlog_id
from .shared.config import get_settings
from .shared.logger import Logger
from datetime import datetime, timedelta
from .pets.service import PetService

logger = Logger(__name__)


def print_paths():
    """Print paths"""
    settings = get_settings()
    logger.info("Token path: %s", settings.TOKEN_PATH)
    logger.info("Credentials path: %s", settings.CREDENTIALS_PATH)


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
            logger.info(
                "%s - %s %s - %s - Pet: %s - awaiting vaccination",
                owner.username,
                owner.first_name,
                owner.last_name,
                owner.email,
                pet.name,
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
                logger.info(
                    "Owner: %s %s, Pet: %s, awaiting vaccination",
                    owner.first_name,
                    owner.last_name,
                    pet.name,
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
            logger.info("no new vaccinations were found")
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
            logger.info(event)


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
        logger.info("Found %s pending dewormings", len(required_dewormings))

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
            logger.info(event)


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


def list_surgeries_without_logs(
    calendar: Calendar = None, service: PetService = None, language: str = "en"
):
    """List surgeries from last 7 days without medical logs"""
    if calendar is None:
        calendar = Calendar()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)

    logger.info(
        "Listing surgeries without logs from %s to %s",
        date_helper.format_date(start_date),
        date_helper.format_date(end_date),
    )

    surgeries = calendar.list_surgeries()
    for surgery in surgeries:
        surgery_date = surgery.get("start").get("dateTime")

        logger.info(
            "Surgery: %s, Date: %s",
            surgery.get("summary"),
            date_helper.format_date(surgery_date),
        )

    if not surgeries:
        logger.info("No surgeries found in the last 7 days")
        return

    with get_session() as session:
        if service is None:
            pet_repo = PetRepository(session)
            service = PetService(pet_repo)

        helper = Helper(pet=None, vaccination=None, owner=None, language=language)
        event = helper.get_missing_pet_logs_event(surgeries)
        for surgery in surgeries:
            try:
                description = surgery.get("description", "")
                logger.info("Reading description: %s", description)
                pet_id = get_vetlog_id(description)
                logs = service.get_logs_by_date_range(
                    start_date, end_date, pet_id=pet_id
                )
                for log in logs:
                    logger.info(
                        "Found log with id: %s, date: %s",
                        log.id,
                        date_helper.format_date(log.date_created),
                    )
            except ValueError as e:
                logger.info(
                    "Error reading description: %s setting logs to empty list", e
                )
                logs = []

            if not logs:
                logger.info("Found %s surgeries without medical logs", len(surgeries))
                calendar.create_event(event)


def surgeries_cli():
    """CLI entry point for surgeries without logs"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language",
        type=str.lower,
        choices=["en", "es"],
        default="en",
        help="Language for the calendar events",
    )
    args = parser.parse_args()
    list_surgeries_without_logs(language=args.language)


def version_check():
    """Print version info"""
    logger.info("%s version %s", __project__, __version__)
