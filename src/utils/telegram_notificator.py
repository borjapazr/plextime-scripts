from typing import Optional

from requests import get

from src.config.constants import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID


class TelegramNotificator:
    def __init__(
        self,
        token: Optional[str] = TELEGRAM_BOT_TOKEN,
        channel_id: Optional[str] = TELEGRAM_CHANNEL_ID,
    ) -> None:
        self.token = token
        self.channel_id = channel_id

    def send_notification(self, message: str) -> None:
        if self.token and self.channel_id:
            get(
                f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.channel_id}&text={message}"  # noqa
            )
