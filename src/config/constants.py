from os import getenv

PLEXTIME_API_URL = "https://plextime.plexus.services/api/v1/"
PLEXTIME_LOGIN_PATH = "admin/login"
PLEXTIME_CHECKIN_PATH = "checkin_noloc"
PLEXTIME_CHECKOUT_PATH = "checkout_noloc"
PLEXTIME_HOLIDAYS_PATH = "admin/company/{company_id}/locality/{locality_id}/holidays"
PLEXTIME_VACATIONS_PATH = (
    "vacations/company/{company_id}/user/{user_id}?begin={date_from}&end={date_to}"
)
PLEXTIME_DAY_INFO_PATH = "admin/company/{company_id}/users/{user_id}/day/{target_day}"
PLEXTIME_TIMETABLES_PATH = "admin/company/{company_id}/users/{user_id}/timetable"
PLEXTIME_LAST_TIMETABLE_PATH = (
    "admin/company/{company_id}/users/{user_id}/last-timetable"
)
PLEXTIME_TIMETABLE_PATH = "admin/company/{company_id}/timetable/{timetable_id}"
PLEXTIME_JOURNAL_OPTIONS_PATH = "admin/company/{company_id}/journal_options"
PLEXTIME_CRYPTO_KEY = "jP=P^=v2AqmNZR6f"
PLEXTIME_API_KEY = "APwXk+7JM7yvqHNNGeeBj8XSRq!$U*@-zKVtQfp_97DJL-bJ3vcW!!AfaTn!eBX47cYk+BPRa94p%e3ZEs2hpV2K=hrwcHsJasZLhX7ycgd6JJ+u4rw?eezAPKUv^TrB2aQXcJSj+Tv#nkL*CF+pm5gx$xGwSznZNZF#VZvfEmnMQ-KuM$D5zADEPS&V*Hah!DgE#-4qB7c25XaDnve_66a=WVBJtjrY^GUMztbuW3_2SdxfUs!TjuBL&Q$5!gHU"  # noqa
PLEXTIME_USER = getenv("PLEXTIME_USER", None)
PLEXTIME_PASSWORD = getenv("PLEXTIME_PASSWORD", None)
CHECKIN_JOURNAL_OPTION = getenv("CHECKIN_JOURNAL_OPTION", 8)
CHECKOUT_JOURNAL_OPTION = getenv("CHECKOUT_JOURNAL_OPTION", 8)
PLEXTIME_HEADERS = {
    "Content-Type": "application/json",
    "api-key": PLEXTIME_API_KEY,
}
CHECKIN_MESSAGE = "↘️ Check-in to work successfully completed on {checkin_datetime}"
CHECKOUT_MESSAGE = "↙️ Check-out to work successfully completed on {checkout_datetime}"
CHECKIN_RANDOM_MARGIN = int(getenv("CHECKIN_RANDOM_MARGIN", 0))
CHECKOUT_RANDOM_MARGIN = int(getenv("CHECKOUT_RANDOM_MARGIN", 0))
TELEGRAM_NOTIFICATIONS = getenv("TELEGRAM_NOTIFICATIONS", "false") == "true"
TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN", None)
TELEGRAM_CHANNEL_ID = getenv("TELEGRAM_CHANNEL_ID", None)
INTERNAL_SCHEDULING = getenv("INTERNAL_SCHEDULING", "false") == "true"
