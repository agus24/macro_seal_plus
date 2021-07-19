import importlib
import requests
import config

importlib.reload(config)


def send_message(message):
    requests.post(config.discord_webhook, data={'content': message})

def send_to_cegel_webhook(message):
    requests.post(config.cegel_webhook, data={'content': message})
