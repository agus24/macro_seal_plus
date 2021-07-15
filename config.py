from core.constants import *


update_before_start = True
dont_sell_items = [SRS, NS]
should_save_to_bank = [SRS, NS]

discord_webhook = "https://discordapp.com/api/webhooks/802486083295379467/x0D2eX1Nqk4_50ugiFGvimGVjblH6QEscfKSJca46PVIftRXA3IpgNN1o6re2VDPPrpF"
log_to_file = True

# auto_purchase_account
username = "",
password = ""
password_bank = ""

try:
    import config_local
except ImportError:
    pass
