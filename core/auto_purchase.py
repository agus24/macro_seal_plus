import requests


username = "agus244"
password = "rahasia"
password_bank = "1111"

ITEM = {
    "pd": 33,
    "grs": 36,
    "atb": 440,
    "brs": 74,
    "wrs": 75,
    "diamond": 67
}

def get_cookies():
    url = "https://seal-gladius.com/login"
    data = {
        "username": username,
        "password": password,
        "is_ajax": 1
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.cookies

    return None

def purchase(item_id, qty=1):
    cookies = get_cookies()
    if not cookies:
        print("failed purchase")
        return None

    more_qty = 0
    purchased_qty = 0

    if item_id == ITEM['atb']:
        url = "https://seal-gladius.com/itemmall-bayar"
        more_qty = 10
    elif item_id == ITEM['pd'] or item_id == ITEM['grs']:
        url = "https://seal-gladius.com/itemmall-bayarrr"
    else:
        url = "https://seal-gladius.com/itemmall-bayarr"

    data = {
        "passbank": password_bank,
        "idmall": item_id,
        "is_ajax": 1
    }

    for _ in range(0, qty + more_qty):
        response = requests.post(url, data=data, cookies=cookies)
        if response.status_code == 200:
            content = response.content.decode("utf-8")
            if "Success" in content:
                purchased_qty += 1
                print("SUKSES PURCHASE")
            elif "purchase limit" in content:
                print("purchase limit reached")
                return False, True, purchased_qty
        else:
            return False, False, purchased_qty

    return True, False, purchased_qty
