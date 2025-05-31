import requests
from config import CONFIG

def create_fastmail_alias(
    puppet_name: str,
    text_signature: str = "",
    html_signature: str = "",
    is_default: bool = False
) -> str:
    """
    Creates a Fastmail alias for the given puppet name using Fastmail's JMAP API.
    If the alias already exists, returns the existing alias email address.
    
    Requires in CONFIG:
        - fastmail_username
        - fastmail_api_token (App Password)
        - fastmail_api_base_url (e.g., 'https://api.fastmail.com/jmap')
        - fastmail_domain (e.g., 'fastmail.com')
    
    Args:
        puppet_name (str): The puppet's name.
        text_signature (str): Plain text signature for the alias.
        html_signature (str): HTML signature for the alias.
        is_default (bool): Whether the alias should be set as the default identity.
    
    Returns:
        str: The created or existing Fastmail alias email address.
    
    Raises:
        Exception: If alias creation fails.
    """
    # Sanitize and prepare alias local part
    local_part = (
        puppet_name.lower()
        .replace(" ", ".")
        .replace("'", "")
        .replace('"', "")
    )
    domain = CONFIG.get("fastmail_domain", "fastmail.com")
    alias_email = f"{local_part}@{domain}"

    headers = {
        "Authorization": f"Bearer {CONFIG['fastmail_api_token']}",
        "Content-Type": "application/json"
    }
    jmap_url = CONFIG["fastmail_api_base_url"].rstrip("/") + "/jmap"

    # Step 1: Fetch all identities to check if alias already exists
    try:
        get_call = [
            [
                "Identity/get",
                {
                    "properties": ["email"]
                },
                "c1"
            ]
        ]
        resp = requests.post(
            jmap_url,
            json={
                "using": [
                    "urn:ietf:params:jmap:core",
                    "urn:ietf:params:jmap:mail"
                ],
                "methodCalls": get_call
            },
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        identities = []
        if "methodResponses" in data and data["methodResponses"]:
            identities = data["methodResponses"][0][1].get("list", [])
        for identity in identities:
            if identity.get("email", "").lower() == alias_email:
                # Alias already exists
                return alias_email
    except Exception as e:
        print(f"Error checking existing Fastmail aliases: {e}")
        raise

    # Step 2: Create alias using JMAP Identity/set
    jmap_set_call = [
        [
            "Identity/set",
            {
                "create": {
                    "newAlias": {
                        "email": alias_email,
                        "mayDelete": True,
                        "sendMail": False,
                        "textSignature": text_signature,
                        "htmlSignature": html_signature,
                        "isDefault": is_default
                    }
                }
            },
            "c2"
        ]
    ]

    try:
        resp = requests.post(
            jmap_url,
            json={
                "using": [
                    "urn:ietf:params:jmap:core",
                    "urn:ietf:params:jmap:mail"
                ],
                "methodCalls": jmap_set_call
            },
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        if "methodResponses" in data and data["methodResponses"]:
            return alias_email
        else:
            raise Exception(f"Failed to create alias: {data}")
    except Exception as e:
        print(f"Error creating Fastmail alias: {e}")
        raise
