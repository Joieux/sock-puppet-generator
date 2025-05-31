# ⚙️ Configuration

All configurable options are stored in `config.py`:

- `openai_api_key`: API key for LLM-powered bio generation
- `fastmail_username`: Your Fastmail username for alias creation (from environment variable or config file)
- `fastmail_api_token`: Fastmail app password/token for JMAP API (from environment variable or config file)
- `fastmail_api_base_url`: Fastmail JMAP endpoint (default: `https://api.fastmail.com/jmap`)
- `fastmail_domain`: Domain for alias emails (default: `fastmail.com`)
- `local_llm_endpoint`: Endpoint for Ollama or LM Studio
- `use_local_llm`: Whether to use a local LLM (True/False)
- `use_tor_proxy`: Route requests through Tor for anonymity (True/False)
- `tor_socks_proxy`: SOCKS proxy address for Tor
- `timeout`: Network timeout in seconds
- `user_agent`: Custom user agent for HTTP requests

## Environment Variables

You can store your secrets and configuration in a `.env` file (see `.env.example`). The application will load these automatically if [python-dotenv](https://pypi.org/project/python-dotenv/) is installed.

**Example:**
```env
OPENAI_API_KEY=sk-...
FASTMAIL_USERNAME=your_fastmail_user
FASTMAIL_API_TOKEN=your_fastmail_app_password
FASTMAIL_API_BASE_URL=https://api.fastmail.com/jmap
FASTMAIL_DOMAIN=fastmail.com
USE_LOCAL_LLM=True
LOCAL_LLM_ENDPOINT=http://localhost:11434/api/generate
USE_TOR_PROXY=True
TOR_SOCKS_PROXY=socks5h://127.0.0.1:9050
TIMEOUT=10
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0
```

> **Security tip:** Never commit your real `.env` file or API keys to a public repository. Only commit `.env.example` and update it with any new configuration options.

## Changing Configurations

1. Edit your `.env` file with the desired values, or update `config.py` defaults.
2. Restart the application for changes to take effect.

For details on available options, see `config.py`.
