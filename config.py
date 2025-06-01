import os

# Try to load dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, will use environment variables directly
    pass

# Configuration settings
CONFIG = {
    # OpenAI API Configuration
    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    
    # LLM Configuration
    "use_local_llm": os.getenv("USE_LOCAL_LLM", "False").lower() == "true",
    "local_llm_endpoint": os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:11434/api/generate"),
    
    # Proxy Configuration
    "use_tor_proxy": os.getenv("USE_TOR_PROXY", "False").lower() == "true",
    "tor_socks_proxy": os.getenv("TOR_SOCKS_PROXY", "socks5h://127.0.0.1:9050"),
    
    # FastMail Configuration
    "fastmail_username": os.getenv("FASTMAIL_USERNAME", ""),
    "fastmail_password": os.getenv("FASTMAIL_PASSWORD", ""),
    "fastmail_domain": os.getenv("FASTMAIL_DOMAIN", "fastmail.com"),
    
    # General Settings
    "default_user_agent": os.getenv("DEFAULT_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"),
    "request_timeout": int(os.getenv("REQUEST_TIMEOUT", "30")),
    "max_retries": int(os.getenv("MAX_RETRIES", "3")),
    
    # Streamlit Configuration
    "debug_mode": os.getenv("DEBUG_MODE", "False").lower() == "true",
    "app_title": os.getenv("APP_TITLE", "Sock Puppet Generator"),
}

# Validate critical settings
if not CONFIG["openai_api_key"] and CONFIG.get("use_local_llm", False) is False:
    print("Warning: No OpenAI API key found and local LLM not enabled")

# Export for easy access
def get_config():
    return CONFIG
