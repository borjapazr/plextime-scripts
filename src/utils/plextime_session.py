from datetime import date, datetime
from json import dumps
from typing import Any, Callable, List, Optional, Union

from requests import get, put

from src.config.constants import (
    CHECKIN_JOURNAL_OPTION,
    CHECKOUT_JOURNAL_OPTION,
    PLEXTIME_API_URL,
    PLEXTIME_CHECKIN_PATH,
    PLEXTIME_CHECKOUT_PATH,
    PLEXTIME_CRYPTO_KEY,
    PLEXTIME_DAY_INFO_PATH,
    PLEXTIME_HEADERS,
    PLEXTIME_HOLIDAYS_PATH,
    PLEXTIME_JOURNAL_OPTIONS_PATH,
    PLEXTIME_LOGIN_PATH,
    PLEXTIME_PASSWORD,
    PLEXTIME_TIMETABLE_PATH,
    PLEXTIME_TIMETABLES_PATH,
    PLEXTIME_USER,
    PLEXTIME_VACATIONS_PATH,
)
from src.utils.aes_cipher import AESCipher
from src.utils.logger import PlxLogger

LOGGER = PlxLogger.get_logger("plextime_session")

DATE_EXPRESSION = "%Y-%m-%d"
DATETIME_EXPRESSION = "%Y-%m-%d %H:%M:%S"


def check_token(func: Callable) -> Callable:
    def inner(self: Any, *args: Any, **kwargs: Any) -> Any:
        if self.token is None:
            LOGGER.error("You must be authenticated")
        else:
            return func(self, *args, **kwargs)

    return inner


class PlextimeSession:
    def __init__(
        self,
        username: Optional[str] = PLEXTIME_USER,
        password: Optional[str] = PLEXTIME_PASSWORD,
        checkin_journal_option: Union[str, int] = CHECKIN_JOURNAL_OPTION,
        checkout_journal_option: Union[str, int] = CHECKOUT_JOURNAL_OPTION,
    ) -> None:
        self.token = None
        self.user_id = None
        self.company_id = None
        self.locality_id = None
        self.holidays: List[date]
        self.vacations: List[List[date]]
        self.checkin_journal_option = checkin_journal_option
        self.checkout_journal_option = checkout_journal_option
        self.origin = 2

        if username and password:
            self.login(username, password)

    def login(self, username: str, password: str) -> None:
        login_data = {"email": username, "password": password}
        login_response = put(
            url=PLEXTIME_API_URL + PLEXTIME_LOGIN_PATH,
            json=self._generate_body(login_data),
            headers=PLEXTIME_HEADERS,
        )

        if login_response.ok and login_response.json()["result"] == "OK":
            self.token = login_response.json()["token"]
            self.user_id = login_response.json()["user_id"]
            self.company_id = login_response.json()["company_id"]
            self.locality_id = login_response.json()["locality_id"]

            PLEXTIME_HEADERS["Authorization"] = self.token

            holidays_response = get(
                url=PLEXTIME_API_URL
                + PLEXTIME_HOLIDAYS_PATH.format(
                    company_id=self.company_id, locality_id=self.locality_id
                ),
                headers=PLEXTIME_HEADERS,
            )

            if holidays_response.ok:
                self.holidays = [
                    datetime.strptime(d["begins"].split(" ")[0], DATE_EXPRESSION).date()
                    for d in holidays_response.json()
                ]

            first_day_year = (
                datetime.now().replace(month=1, day=1).date().strftime(DATE_EXPRESSION)
            )
            last_day_year = (
                datetime.now()
                .replace(month=12, day=31)
                .date()
                .strftime(DATE_EXPRESSION)
            )
            vacations_response = get(
                url=PLEXTIME_API_URL
                + PLEXTIME_VACATIONS_PATH.format(
                    company_id=self.company_id,
                    user_id=self.user_id,
                    date_from=first_day_year,
                    date_to=last_day_year,
                ),
                headers=PLEXTIME_HEADERS,
            )

            if vacations_response.ok:
                self.vacations = [
                    [
                        datetime.strptime(
                            d["init_date"].split(" ")[0], DATE_EXPRESSION
                        ).date(),
                        datetime.strptime(
                            d["end_date"].split(" ")[0], DATE_EXPRESSION
                        ).date(),
                    ]
                    for d in vacations_response.json()["requests"]
                ]

        else:
            LOGGER.error("Authentication failed")

    @check_token
    def retrieve_journal_options(self) -> Optional[dict]:
        if self.token:
            journal_options_response = get(
                url=PLEXTIME_API_URL
                + PLEXTIME_JOURNAL_OPTIONS_PATH.format(company_id=self.company_id),
                headers=PLEXTIME_HEADERS,
            )

            if journal_options_response.ok:
                return journal_options_response.json()["journal_options"]
        return None

    @check_token
    def retrieve_current_timetable(self) -> Optional[dict]:
        if self.token:
            timetables_response = get(
                url=PLEXTIME_API_URL
                + PLEXTIME_TIMETABLES_PATH.format(
                    company_id=self.company_id, user_id=self.user_id
                ),
                headers=PLEXTIME_HEADERS,
            )

            if timetables_response.ok:
                timetables = (
                    timetables_response.json()["timetable"]
                    if timetables_response.json()["timetable"]
                    else None
                )

                if timetables:
                    today = datetime.now().date()
                    for timetable in timetables:
                        if not timetable["status"]:
                            continue

                        if (
                            timetable["init_date"] is None
                            and timetable["end_date"] is None
                        ):
                            current_timetable = timetable["id"]
                        else:
                            init_date = datetime.strptime(
                                timetable["init_date"].split(" ")[0], DATE_EXPRESSION
                            ).date()
                            end_date = datetime.strptime(
                                timetable["end_date"].split(" ")[0], DATE_EXPRESSION
                            ).date()

                            if init_date <= today <= end_date:
                                current_timetable = timetable["id"]

                    timetable_response = get(
                        url=PLEXTIME_API_URL
                        + PLEXTIME_TIMETABLE_PATH.format(
                            company_id=self.company_id, timetable_id=current_timetable
                        ),
                        headers=PLEXTIME_HEADERS,
                    )

                    if timetable_response.ok:
                        return timetable_response.json()["times"]
        return None

    @check_token
    def checkin_if_working_day_and_not_checkedin_before(self) -> bool:
        today = datetime.now().date()
        if (
            self.token
            and not any(d == today for d in self.holidays)
            and not any(d[0] <= today <= d[1] for d in self.vacations)
        ):

            current_day_info_response = get(
                url=PLEXTIME_API_URL
                + PLEXTIME_DAY_INFO_PATH.format(
                    company_id=self.company_id,
                    user_id=self.user_id,
                    target_day=today.strftime(DATE_EXPRESSION),
                ),
                headers=PLEXTIME_HEADERS,
            )

            if current_day_info_response.ok:
                last_checkin = [
                    x
                    for x in current_day_info_response.json()["checks"]
                    if x["checkout"] is None
                ]
                last_checkin = last_checkin[0] if len(last_checkin) == 1 else None

                if last_checkin is None:
                    checkin_data = {
                        "iduser": self.user_id,
                        "date": datetime.utcnow().strftime(DATETIME_EXPRESSION),
                        "optionId": self.checkin_journal_option,
                        "origin": self.origin,
                    }

                    checkin_response = put(
                        url=PLEXTIME_API_URL + PLEXTIME_CHECKIN_PATH,
                        json=self._generate_body(checkin_data),
                        headers=PLEXTIME_HEADERS,
                    )

                    return (
                        checkin_response.ok
                        and checkin_response.json()["result"] == "OK"
                    )
        return False

    @check_token
    def checkout_if_checkedin_before(self) -> bool:
        today = datetime.now().date()
        if (
            self.token
            and not any(d == today for d in self.holidays)
            and not any(d[0] <= today <= d[1] for d in self.vacations)
        ):
            current_day_info_response = get(
                url=PLEXTIME_API_URL
                + PLEXTIME_DAY_INFO_PATH.format(
                    company_id=self.company_id,
                    user_id=self.user_id,
                    target_day=today.strftime(DATE_EXPRESSION),
                ),
                headers=PLEXTIME_HEADERS,
            )

            if current_day_info_response.ok:
                last_checkin = [
                    x
                    for x in current_day_info_response.json()["checks"]
                    if x["checkout"] is None
                ]
                last_checkin = last_checkin[0] if len(last_checkin) == 1 else None

                if last_checkin:
                    checkout_data = {
                        "id": last_checkin["id"],
                        "iduser": self.user_id,
                        "date": datetime.utcnow().strftime(DATETIME_EXPRESSION),
                        "optionId": self.checkout_journal_option,
                        "origin": self.origin,
                    }

                    checkout_response = put(
                        url=PLEXTIME_API_URL + PLEXTIME_CHECKOUT_PATH,
                        json=self._generate_body(checkout_data),
                        headers=PLEXTIME_HEADERS,
                    )

                    return (
                        checkout_response.ok
                        and checkout_response.json()["result"] == "OK"
                    )
        return False

    @staticmethod
    def _generate_body(data: dict) -> dict:
        return {
            "value": AESCipher(PLEXTIME_CRYPTO_KEY).encrypt(dumps(dumps(data))).decode()
        }
