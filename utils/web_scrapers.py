import requests

def get_fake_identity(proxy=False):
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050',
    } if proxy else None

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        print("Trying elfqrin.com...")
        response = requests.get(
            'https://www.elfqrin.com/fake-identities-eu',
            headers=headers,
            proxies=proxies,
            timeout=10
        )
        response.raise_for_status()
        # 🟡 You'll still need to parse the HTML if elfqrin works.
        return {"source": "elfqrin", "raw_html": response.text}

    except Exception as e:
        print(f"elfqrin.com failed: {e}")
        print("Falling back to randomuser.me...")

        try:
            response = requests.get("https://randomuser.me/api/", timeout=10)
            response.raise_for_status()
            data = response.json()
            user = data['results'][0]
            return {
                "source": "randomuser",
                "name": f"{user['name']['first']} {user['name']['last']}",
                "email": user['email'],
                "username": user['login']['username'],
                "password": user['login']['password'],
                "address": f"{user['location']['street']['number']} {user['location']['street']['name']}, {user['location']['city']}, {user['location']['country']}",
                "phone": user['phone'],
                "dob": user['dob']['date']
            }

        except Exception as e2:
            raise RuntimeError(f"Both identity sources failed: {e2}")
