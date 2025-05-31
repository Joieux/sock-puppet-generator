import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

CONFIG = {
    "openai_api_key": os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_KEY_HERE"),
    "fastmail_username": os.getenv("FASTMAIL_USERNAME", "your_fastmail_user"),
    # This should be your Fastmail app password (token), not your regular password!
    "fastmail_api_token": os.getenv("FASTMAIL_API_TOKEN", "your_fastmail_app_password"),
    "fastmail_api_base_url": os.getenv("FASTMAIL_API_BASE_URL", "https://api.fastmail.com/jmap"),
    "fastmail_domain": os.getenv("FASTMAIL_DOMAIN", "fastmail.com"),
    "use_local_llm": os.getenv("USE_LOCAL_LLM", "True").lower() == "true",
    "local_llm_endpoint": os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:11434/api/generate"),
    "use_tor_proxy": os.getenv("USE_TOR_PROXY", "True").lower() == "true",
    "tor_socks_proxy": os.getenv("TOR_SOCKS_PROXY", "socks5h://127.0.0.1:9050"),
    "timeout": int(os.getenv("TIMEOUT", "10")),
    "user_agent": os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0"
    )
}
