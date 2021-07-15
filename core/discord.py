import requests
import config


def send_message(message):
    requests.post(config.discord_webhook, data={'content': message})
