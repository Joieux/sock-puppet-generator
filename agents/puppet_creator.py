import requests
import sqlite3
from io import BytesIO
from typing import Optional, Dict, Any
from utils.web_scrapers import get_fake_identity
from mail_utils.fastmail_api import create_fastmail_alias
from config import CONFIG

def get_face_image() -> Optional[BytesIO]:
    url = "https://thispersondoesnotexist.com/image"
    proxies = {"http": CONFIG["tor_socks_proxy"], "https": CONFIG["tor_socks_proxy"]} if CONFIG.get("use_tor_proxy") else None
    headers = {"User-Agent": CONFIG["user_agent"]}
    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=CONFIG["timeout"])
        r.raise_for_status()
        return BytesIO(r.content)
    except requests.RequestException as e:
        print(f"❌ Failed to get face image: {e}")
        return None

def generate_bio(identity: Dict[str, Any]) -> str:
    prompt = (
        f"Generate a brief bio for a person named {identity['name']} "
        f"living in {identity.get('location', 'an unknown location')}. "
        f"Interests: {', '.join(identity.get('interests', ['unknown']))}"
    )
    if CONFIG.get("use_local_llm"):
        try:
            r = requests.post(CONFIG["local_llm_endpoint"], json={"prompt": prompt})
            r.raise_for_status()
            return r.text.strip()
        except requests.RequestException as e:
            print(f"❌ Local LLM error: {e}")
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
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            return "Bio unavailable."

def fetch_identity_from_randomuser() -> Optional[Dict[str, Any]]:
    try:
        response = requests.get("https://randomuser.me/api/")
        response.raise_for_status()
        user_data = response.json()["results"][0]
        return {
            "name": f"{user_data['name']['first']} {user_data['name']['last']}",
            "dob": user_data["dob"]["date"],
            "location": f"{user_data['location']['city']}, {user_data['location']['country']}",
            "email": user_data["email"],
            "interests": ["Reading", "Traveling", "Music"]
        }
    except requests.RequestException as e:
        print(f"❌ Failed to fetch identity from randomuser.me: {e}")
        return None

def generate_sock_puppet():
    try:
        identity = get_fake_identity(proxy=False)
        if not identity:
            print("⚠️ get_fake_identity failed, falling back to randomuser.me.")
            identity = fetch_identity_from_randomuser()
            if not identity:
                print("❌ Failed to obtain identity.")
                return None

        image_data = get_face_image()
        if not image_data:
            print("❌ Failed to fetch face image.")
            return None

        # Normalize 'name' field if missing
        if 'name' not in identity:
            if 'first' in identity and 'last' in identity:
                identity['name'] = f"{identity['first']} {identity['last']}"
            elif 'results' in identity and len(identity['results']) > 0:
                name_data = identity['results'][0].get('name', {})
                first = name_data.get('first')
                last = name_data.get('last')
                if first and last:
                    identity['name'] = f"{first} {last}"
                else:
                    identity['name'] = "Unknown"
            else:
                identity['name'] = "Unknown"

        # Assume create_fastmail_alias and generate_bio exist and work
        email = create_fastmail_alias(identity["name"])
        if not email:
            print("❌ Failed to generate email alias.")
            return None

        bio = generate_bio(identity)
        if not bio or bio == "Bio unavailable.":
            print("❌ Bio generation failed.")
            return None

        puppet = {
            "name": identity["name"],
            "dob": identity.get("dob", "Unknown"),
            "location": identity.get("location", "Unknown"),
            "email": email,
            "interests": identity.get("interests", []),
            "photo": image_data,
            "bio": bio,
            "source": {
                "face": "ThisPersonDoesNotExist",
                "identity": identity.get("source", "unknown"),
                "email": "Fastmail"
            }
        }

        # You can add save_puppet_to_db(puppet) here if desired

        return puppet

    except Exception as e:
        print("❌ Error during puppet generation:", e)
        return None


def save_puppet_to_db(puppet: Dict[str, Any]):
    try:
        conn = sqlite3.connect("puppets.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS puppets (
                            name TEXT,
                            dob TEXT,
                            location TEXT,
                            email TEXT,
                            interests TEXT,
                            photo BLOB,
                            bio TEXT,
                            source TEXT)''')
        cursor.execute('''INSERT INTO puppets (name, dob, location, email, interests, photo, bio, source)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
            puppet["name"],
            puppet["dob"],
            puppet["location"],
            puppet["email"],
            ", ".join(puppet["interests"]),
            puppet["photo"].getvalue(),
            puppet["bio"],
            str(puppet["source"])
        ))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Failed to save puppet to database: {e}")
