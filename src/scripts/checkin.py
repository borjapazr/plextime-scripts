#!/usr/bin/env python3

"""
Script for automatic checking in to Plexus Tech
"""

from time import sleep
from random import randint
from datetime import datetime

from src.config.constants import CHECKIN_RANDOM_MARGIN, TELEGRAM_NOTIFICATIONS, CHECKIN_MESSAGE
from src.utils.plextime_session import PlextimeSession
from src.utils.telegram_notificator import TelegramNotificator
from src.utils.logger import PlxLogger

LOGGER = PlxLogger.get_logger("checkin")


def checkin():
    if PlextimeSession().checkin_if_working_day_and_not_checkedin_before():
        checkin_message = CHECKIN_MESSAGE.format(
            checkin_datetime=datetime.now().strftime("%d/%m/%Y at %H:%M:%S"))
        LOGGER.info(checkin_message)
        if TELEGRAM_NOTIFICATIONS:
            TelegramNotificator().send_notification(checkin_message)


def random_checkin():
    sleep(randint(0, CHECKIN_RANDOM_MARGIN))
    checkin()


def main():
    checkin()


if __name__ == '__main__':
    main()
