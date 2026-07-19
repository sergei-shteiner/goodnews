import os

import requests
from dotenv import find_dotenv, load_dotenv


_ = load_dotenv(find_dotenv())

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"
TELEGRAM_MESSAGE_LIMIT = 4096


def is_telegram_configured():
    return bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID)


def _split_message(text, limit=TELEGRAM_MESSAGE_LIMIT):
    if len(text) <= limit:
        return [text]

    parts = []
    remaining = text
    while remaining:
        chunk = remaining[:limit]
        split_at = chunk.rfind("\n\n")
        if split_at <= 0:
            split_at = chunk.rfind("\n")
        if split_at <= 0:
            split_at = limit

        parts.append(remaining[:split_at].strip())
        remaining = remaining[split_at:].strip()

    return parts


def publish_news(message):
    if not is_telegram_configured():
        return False

    url = TELEGRAM_API_URL.format(token=TELEGRAM_BOT_TOKEN)
    for part in _split_message(message):
        response = requests.post(
            url,
            json={
                "chat_id": TELEGRAM_CHANNEL_ID,
                "text": part,
                "disable_web_page_preview": True,
            },
            timeout=10,
        )
        response.raise_for_status()

    return True
