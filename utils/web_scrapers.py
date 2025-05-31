import requests
from bs4 import BeautifulSoup
from config import CONFIG
import random

def get_fake_identity(proxy=True):
    """
    Scrapes a fake identity from ElfQrin for sock puppet generation.

    Args:
        proxy (bool): Whether to use the Tor proxy. Default is True.

    Returns:
        dict: A dictionary containing fake name, dob, location, interests, and source.
    """
    proxies = (
        {"http": CONFIG["tor_socks_proxy"], "https": CONFIG["tor_socks_proxy"]}
        if proxy and CONFIG.get("use_tor_proxy", False)
        else None
    )
    headers = {"User-Agent": CONFIG["user_agent"]}
    url = "https://www.elfqrin.com/fake-identities-eu"

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=CONFIG["timeout"])
        response.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch fake identity: {e}")

    soup = BeautifulSoup(response.content, "html.parser")

    # Try to extract the name robustly
    name_tag = soup.find("h4")
    name = name_tag.text.strip() if name_tag else "John Doe"

    # You might want to parse location and dob from the page if you want more realism
    # For now, keep the fixed Amsterdam, NL and generate a plausible DoB
    location = "Amsterdam, NL"
    dob = f"19{random.randint(70, 99)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

    interests_pool = ["OSINT", "crypto", "infosec", "coding", "anonymity", "privacy", "journalism", "travel", "sports"]
    interests = random.sample(interests_pool, 3)

    return {
        "name": name,
        "dob": dob,
        "location": location,
        "interests": interests,
        "source": "ElfQrin"
    }
