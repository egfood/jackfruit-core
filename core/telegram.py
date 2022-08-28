from typing import Optional
from urllib.parse import ParseResult

from django.conf import settings


def get_tg_link() -> Optional[ParseResult]:
    tg_link = settings.TELEGRAM_CHANNEL_LINK
    return tg_link.geturl() if isinstance(tg_link, ParseResult) else None
