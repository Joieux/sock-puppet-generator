# sockpuppet_agent/agents/puppet_creator.py
import requests
import random
from utils.web_scrapers import get_fake_identity
from email.fastmail_api import create_fastmail_alias
from config import CONFIG
from io import BytesIO


def get_face_image():
    url = "https://thispersondoesnotexist.com/image"
    proxies = {"http": CONFIG["tor_socks_proxy"], "https": CONFIG["tor_socks_proxy"]} if CONFIG["use_tor_proxy"] else None
    headers = {"User-Agent": CONFIG["user_agent"]}
    r = requests.get(url, headers=headers, proxies=proxies, timeout=CONFIG["timeout"])
    return BytesIO(r.content)


def generate_bio(identity):
    if CONFIG["use_local_llm"]:
        prompt = f"Generate a brief bio for a person named {identity['name']} living in {identity['location']}. Interests: {identity['interests']}"
        r = requests.post(CONFIG["local_llm_endpoint"], json={"prompt": prompt})
        return r.text.strip()
    else:
        import openai
        openai.api_key = CONFIG["openai_api_key"]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a persona generation assistant."},
                {"role": "user", "content": f"Create a bio for someone named {identity['name']} who likes {', '.join(identity['interests'])}."}
            ]
        )
        return response.choices[0].message.content


def generate_sock_puppet(use_openai=True, use_local_llm=True, use_proxy=True):
    identity = get_fake_identity(proxy=use_proxy)
    image_data = get_face_image()
    email = create_fastmail_alias(identity['name'])
    bio = generate_bio(identity)

    return {
        "name": identity["name"],
        "dob": identity["dob"],
        "location": identity["location"],
        "email": email,
        "interests": identity["interests"],
        "photo": image_data,
        "bio": bio,
        "source": {
            "face": "ThisPersonDoesNotExist",
            "identity": identity["source"],
            "email": "Fastmail"
        }
    }
