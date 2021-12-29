from time import sleep

from schedule import clear, every, get_jobs, run_pending

from src.config.constants import INTERNAL_SCHEDULING
from src.scripts.checkin import random_checkin
from src.scripts.checkout import random_checkout
from src.utils.logger import PlxLogger
from src.utils.plextime_session import PlextimeSession

LOGGER = PlxLogger.get_logger("start")

DAYS = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
    7: "sunday",
}


def schedule_tasks():
    if get_jobs("check"):
        LOGGER.info("Cleaning up old schedulings")
        clear("check")

    timetable = PlextimeSession().retrieve_current_timetable()

    if timetable:
        LOGGER.info("Starting scheduling")
        for day_schedule in timetable:
            day_name = DAYS[day_schedule["week_day"]]
            checkin_hour = day_schedule["hour_in"]
            checkout_hour = day_schedule["hour_out"]
            getattr(every(), day_name).at(checkin_hour).do(random_checkin).tag(
                "check", "checkin-tasks"
            )
            getattr(every(), day_name).at(checkout_hour).do(random_checkout).tag(
                "check", "checkout-tasks"
            )
            LOGGER.info(
                f"{day_name.capitalize()} scheduled: check-in at {checkin_hour} and"
                f" check-out at {checkout_hour}"
            )


def main():
    if INTERNAL_SCHEDULING:
        LOGGER.info("Internal scheduling enabled")
        timetable_update_weekday = DAYS[1]
        timetable_update_time = "03:00"
        getattr(every(), timetable_update_weekday).at(timetable_update_time).do(
            schedule_tasks
        ).tag("schedule")
        LOGGER.info(
            "Timetable updating task enabled for"
            f" {timetable_update_weekday.capitalize()}s at {timetable_update_time}"
        )
        schedule_tasks()
        while True:
            run_pending()
            sleep(1)
    else:
        LOGGER.info("Using external scheduling")
        while True:
            LOGGER.info("External scheduling: keep-alive")
            sleep(60 * 60 * 8)


if __name__ == "__main__":
    main()
