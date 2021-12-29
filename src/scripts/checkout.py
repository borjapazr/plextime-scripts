#!/usr/bin/env python3

"""
Script for automatic checking out to Plexus Tech
"""

from datetime import datetime
from random import randint
from time import sleep

from src.config.constants import (
    CHECKIN_RANDOM_MARGIN,
    CHECKOUT_MESSAGE,
    CHECKOUT_RANDOM_MARGIN,
    TELEGRAM_NOTIFICATIONS,
)
from src.utils.logger import PlxLogger
from src.utils.plextime_session import PlextimeSession
from src.utils.telegram_notificator import TelegramNotificator

LOGGER = PlxLogger.get_logger("checkout")


def checkout():
    if PlextimeSession().checkout_if_checkedin_before():
        checkout_message = CHECKOUT_MESSAGE.format(
            checkout_datetime=datetime.now().strftime("%d/%m/%Y at %H:%M:%S")
        )
        LOGGER.info(checkout_message)
        if TELEGRAM_NOTIFICATIONS:
            TelegramNotificator().send_notification(checkout_message)


def random_checkout():
    sleep(
        randint(
            CHECKIN_RANDOM_MARGIN,
            CHECKOUT_RANDOM_MARGIN
            if CHECKIN_RANDOM_MARGIN <= CHECKOUT_RANDOM_MARGIN
            else CHECKIN_RANDOM_MARGIN,
        )
    )
    checkout()


def main():
    checkout()


if __name__ == "__main__":
    main()
