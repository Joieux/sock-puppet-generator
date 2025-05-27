# sockpuppet_agent/config.py

CONFIG = {
    "openai_api_key": "YOUR_OPENAI_KEY_HERE",
    "fastmail_username": "your_fastmail_user",
    "fastmail_password": "your_fastmail_app_password",
    "use_local_llm": True,
    "local_llm_endpoint": "http://localhost:11434/api/generate",
    "use_tor_proxy": True,
    "tor_socks_proxy": "socks5h://127.0.0.1:9050",
    "timeout": 10,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0"
}