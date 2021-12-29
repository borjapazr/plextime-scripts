#!/usr/bin/env python3

"""
Script to retrieve journal options from authenticated user
"""

from src.utils.logger import PlxLogger
from src.utils.plextime_session import PlextimeSession

LOGGER = PlxLogger.get_logger("journal_options")


def retrieve_user_journal_options():
    journal_options = PlextimeSession().retrieve_journal_options()
    if journal_options:
        for option in journal_options:
            print(f'-> {option["name"]}: {option["id"]}')
    else:
        print("No journal options retrieved")


def main():
    retrieve_user_journal_options()


if __name__ == "__main__":
    main()
