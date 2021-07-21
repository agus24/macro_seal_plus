from core.constants import *


update_before_start = True
dont_sell_items = [SRS, NS]
should_save_to_bank = [SRS, NS]

# discord
discord_webhook = "https://discordapp.com/api/webhooks/802486083295379467/x0D2eX1Nqk4_50ugiFGvimGVjblH6QEscfKSJca46PVIftRXA3IpgNN1o6re2VDPPrpF"
cegel_webhook = "https://discord.com/api/webhooks/866752707612508160/zegobzGKiGlrrCscaWdc3abHDiyhB0ljNiu8xAsan-QFAv2vdPzfMtWHSCxsPhKiQAfg"

log_to_file = True

# auto_purchase_account
username = "",
password = ""
password_bank = ""

# auto refine
atb_purchase_qty = 9  # qty atb per beli barang
atb_per_purchase = 4  # qty atb yang digunakan
wrs_brs_diamond_per_purchase = 5  # wrs diamond sekali beli
pd_grs_per_purchase = 5  # pd grs sekali beli
max_tempa = 11  # target tempa (kalo 11 sampe +11 klo 12 sampe +12)

# restock accounts
restock_accounts = [
    {
        "username": "",
        "password": "",
        "password_bank": "",
    }
]

restock_send_to_discord = True
