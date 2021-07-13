import requests


URL = "https://discordapp.com/api/webhooks/802486083295379467/x0D2eX1Nqk4_50ugiFGvimGVjblH6QEscfKSJca46PVIftRXA3IpgNN1o6re2VDPPrpF"

def send_message(message):
    requests.post(URL, data={'content': message})
