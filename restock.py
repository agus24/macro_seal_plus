import requests
import json
import re

from time import sleep
from datetime import datetime
from config import restock_accounts, restock_send_to_discord
from core.logger import Logger


logger = Logger(user_id=0, file_name="restock_check")

targeted_item = [
    {"item_id": 21084, "item_name": "Manual G20"},
    {"item_id": 78057, "item_name": "Refinement GXG1"},
]


def get_active_users():
    users = []
    for user in restock_accounts:
        users.append(user['username'])

    return users

def get_cookies(user):
    url = "https://seal-gladius.com/login"
    data = {
        "username": user['username'],
        "password": user['password'],
        "is_ajax": 1
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.cookies

    return None


def get_item_list():
    cookies = get_cookies(restock_accounts[0])

    url = "https://seal-gladius.com/itemmall-dataa"
    response = requests.post(url, data={"page": 1, "jenis": 7}, cookies=cookies).content.decode("utf-8")
    items = parse_output(response)
    restock_status, restocked_item = check_restock_status(items)

    if restock_status:
        list_of_item = []
        for index, item in enumerate(restocked_item):
            list_of_item.append(f"{item['name']} : {item['qty']} -> {items[index]['qty']}")

        send_discord_message("@everyone\n**Item Restocked**\n\n**List of item:** \n\n" + "\n".join(list_of_item))
        buy_item()

    f = open("restock/_restock_list.json", "w")
    f.write(json.dumps(items, indent=4, sort_keys=True))
    f.close()


def check_restock_status(items):
    print("checking item")
    file = open("restock/_restock_list.json", "r").read()
    restock_list = json.loads(file)
    restocked_item = []

    i = 0
    while i < len(items):
        if items[i]['qty'] > restock_list[i]['qty']:
            restocked_item.append(items[i])
        i += 1

    if len(restocked_item):
        return True, restocked_item
    else:
        return False, restocked_item


def buy_item():
    url = "https://seal-gladius.com/itemmall-bayarr"

    cookies_list = {}
    for i in range(0, 200):
        for user in restock_accounts:
            cookies = get_cookies(user)
            data = {
                "passbank": user['password_bank'],
                "idmall": targeted_item[0]['item_id'],
                "is_ajax": 1
            }

            response = requests.post(url, data=data, cookies=cookies)
            send_discord_message(f"Purchasing item **{targeted_item[0]['item_name']}** for: **{user['username']}**")

            data['idmall'] = targeted_item[1]['item_id']
            response = requests.post(url, data=data, cookies=cookies)
            send_discord_message(f"Purchasing item **{targeted_item[1]['item_name']}** for: **{user['username']}**")


def parse_output(output):
    data = []
    texts = output.split("<td>")
    texts.pop(0)

    for i, text in enumerate(texts):
        if text[:9] == "<img src=":
            del texts[i]

    for i, text in enumerate(texts):
        if text[:9] == "<img src=":
            del texts[i]

    i = 0
    while i < len(texts):
        texts[i] = texts[i].split("</td>")[0]
        texts[i+1] = texts[i+1].split("</td>")[0]
        output = {
            "name": texts[i],
            "qty": int(texts[i+1])
        }
        data.append(output)
        i += 2

    return data


def send_discord_message(message):
    if not restock_send_to_discord:
        return

    time = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M')

    url = "https://discordapp.com/api/webhooks/802558967310057504/DltylKMUlMd0XevzX3NPh1ItQAmLjEmJRPRxvwz2ue9-Xo83Ct58HTVUc0nZCzVU9HQK"
    requests.post(url, data={'content': f"[{time}] {message}"})


def start():
    usernames = ", ".join(get_active_users())
    send_discord_message(f"Starting bot\nusernames : **{usernames}**")
    while True:
        time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
        try:
            get_item_list()
            sleep(2 * 60)
        except KeyboardInterrupt:
            send_discord_message("stopping bot")
            break
        except Exception as e:
            print(e)


start()
