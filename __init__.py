from modules import app, cbpi
from thread import start_new_thread
import logging
import time
import requests

telegram_bot_token = None
telegram_chat_id = None
telegram = None


def telegramBotToken():
    global telegram_bot_token
    telegram_bot_token = cbpi.get_config_parameter("telegram_bot_token", None)
    if telegram_bot_token is None:
        print("INIT Telegram Bot Token")
        try:
            cbpi.add_config_parameter(
                "telegram_bot_token", "", "text", "Telegram Bot Token")
        except:
            cbpi.notify("Telegram Error", "Unable to update database. Update CraftBeerPi and reboot.",
                        type="danger", timeout=None)


def telegramChatId():
    global telegram_chat_id
    telegram_chat_id = cbpi.get_config_parameter("telegram_chat_id", None)
    if telegram_chat_id is None:
        print("INIT Telegram Chat ID")
        try:
            cbpi.add_config_parameter(
                "telegram_chat_id", "", "text", "Telegram Chat ID")
        except:
            cbpi.notify("Telegram Error", "Unable to update database. Update CraftBeerPi and reboot.",
                        type="danger", timeout=None)


@cbpi.initalizer(order=9000)
def init(cbpi):
    global telegram
    cbpi.app.logger.info("INITIALIZE Telegram PLUGIN")
    telegramBotToken()
    telegramChatId()
    if telegram_bot_token is None or not telegram_bot_token:
        cbpi.notify("Telegram Error", "Check that Telegram Bot Token is set",
                    type="danger", timeout=None)
    elif telegram_chat_id is None or not telegram_chat_id:
        cbpi.notify("Telegram Error", "Check that Telegram Chat ID is set",
                    type="danger", timeout=None)
    else:
        telegram = "OK"


@cbpi.event("MESSAGE", async=True)
def messageEvent(message):
    if telegram_bot_token is not None and telegram_chat_id is not None:
        text = "<b>" + message["headline"] + \
            "</b>\n<i>" + message["message"] + "</i>"
        url = "https://api.telegram.org/bot" + telegram_bot_token + "/sendMessage"
        escapedUrl = requests.Request('GET', url,
                                    params={"chat_id": telegram_chat_id,
                                            "text": text,
                                            "parse_mode": "HTML"},
                                    ).prepare().url
        requests.get(escapedUrl)
