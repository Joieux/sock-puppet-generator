import requests
from io import BytesIO
from typing import Optional, Dict, Any

from utils.web_scrapers import get_fake_identity
from mail_utils.fastmail_api import create_fastmail_alias
from config import CONFIG


def get_face_image() -> Optional[BytesIO]:
    """
    Fetches a random face image from thispersondoesnotexist.com using optional Tor proxy.
    Returns:
        BytesIO: Image data in memory, or None if the request fails.
    """
    url = "https://thispersondoesnotexist.com/image"
    proxies = {"http": CONFIG["tor_socks_proxy"], "https": CONFIG["tor_socks_proxy"]} if CONFIG.get("use_tor_proxy") else None
    headers = {"User-Agent": CONFIG["user_agent"]}
    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=CONFIG["timeout"])
        r.raise_for_status()
        return BytesIO(r.content)
    except requests.RequestException as e:
        # Use logging in production
        print(f"Failed to get face image: {e}")
        return None


def generate_bio(identity: Dict[str, Any]) -> str:
    """
    Generates a brief bio for the given identity using either a local LLM or OpenAI.
    Returns:
        str: The generated bio or a fallback message if generation fails.
    """
    prompt = (
        f"Generate a brief bio for a person named {identity['name']} "
        f"living in {identity['location']}. Interests: {', '.join(identity['interests'])}"
    )
    if CONFIG.get("use_local_llm"):
        try:
            r = requests.post(CONFIG["local_llm_endpoint"], json={"prompt": prompt})
            r.raise_for_status()
            return r.text.strip()
        except requests.RequestException as e:
            print(f"Local LLM error: {e}")
            return "Bio unavailable."
    else:
        try:
            import openai
            openai.api_key = CONFIG["openai_api_key"]
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a persona generation assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {e}")
            return "Bio unavailable."


def generate_sock_puppet():
    try:
        print("🔍 Generating fake identity...")
        identity = get_fake_identity(proxy=False)
        print("✅ Identity generated:", identity)

        # You can add more puppet logic here if needed
        puppet = {
            "identity": identity,
            "status": "created"
        }

        return puppet

    except Exception as e:
        print("❌ Error during puppet generation:", e)
        raise  # Re-raise so Streamlit can catch it and show the error

    image_data = get_face_image()
    if not image_data:
        print("Failed to fetch face image.")
        return None

    email = create_fastmail_alias(identity["name"])
    if not email:
        print("Failed to generate email alias.")
        return None

    bio = generate_bio(identity)
    if not bio or bio == "Bio unavailable.":
        print("Bio generation failed.")
        return None

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
            "identity": identity.get("source", "unknown"),
            "email": "Fastmail"
        }
    }
