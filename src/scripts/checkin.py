#!/usr/bin/env python3

"""
Script for automatic checking in to Plexus Tech
"""

from datetime import datetime
from random import randint
from time import sleep

from src.config.constants import (
    CHECKIN_MESSAGE,
    CHECKIN_RANDOM_MARGIN,
    TELEGRAM_NOTIFICATIONS,
)
from src.utils.logger import PlxLogger
from src.utils.plextime_session import PlextimeSession
from src.utils.telegram_notificator import TelegramNotificator

LOGGER = PlxLogger.get_logger("checkin")


def checkin() -> None:
    if PlextimeSession().checkin_if_working_day_and_not_checkedin_before():
        checkin_message = CHECKIN_MESSAGE.format(
            checkin_datetime=datetime.now().strftime("%d/%m/%Y at %H:%M:%S")
        )
        LOGGER.info(checkin_message)
        if TELEGRAM_NOTIFICATIONS:
            TelegramNotificator().send_notification(checkin_message)


def random_checkin() -> None:
    sleep(randint(0, CHECKIN_RANDOM_MARGIN))
    checkin()


def main() -> None:
    checkin()


if __name__ == "__main__":
    main()
