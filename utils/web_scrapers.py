# sockpuppet_agent/utils/web_scrapers.py
import requests
from bs4 import BeautifulSoup
from config import CONFIG
import random

def get_fake_identity(proxy=True):
    proxies = {"http": CONFIG["tor_socks_proxy"], "https": CONFIG["tor_socks_proxy"]} if proxy and CONFIG["use_tor_proxy"] else None
    headers = {"User-Agent": CONFIG["user_agent"]}

    url = "https://www.elfqrin.com/fake-identities-eu"
    response = requests.get(url, headers=headers, proxies=proxies, timeout=CONFIG["timeout"])
    soup = BeautifulSoup(response.content, "html.parser")

    name = soup.find("h4").text.strip()
    location = "Amsterdam, NL"
    dob = f"19{random.randint(70, 99)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    interests = random.sample(["OSINT", "crypto", "infosec", "coding", "anonymity"], 3)

    return {
        "name": name,
        "dob": dob,
        "location": location,
        "interests": interests,
        "source": "ElfQrin"
    }
