# ⚙️ Configuration Guide

## Should I use a `.env` file in this project?

**Yes, using a `.env` file is recommended, but not strictly required.**

### Why use `.env`?

- **Security:** Keeps sensitive keys (API keys, passwords, etc.) out of your codebase.
- **Convenience:** Easily manage and swap configs for different environments (development, production, CI).
- **Best Practice:** Most Python projects use `.env` with libraries like `python-dotenv` to load secrets automatically.

### Where should `.env` go?

Place your `.env` file at the root of your project:

```
sockpuppet_agent/
├── .env           # <-- Place it here
├── main.py
├── config.py
...
```

### Should I commit `.env`?

**No!**  
Add `.env` to your `.gitignore` so it is never committed to version control.

---

## Example `.env`

```
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

---

## How does the project use `.env`?

Your `config.py` loads environment variables via `python-dotenv`. If a variable is not found in `.env`, it uses a default value.

**You can run the project without a `.env` file, but then you must manually edit `config.py` to insert your keys and settings.**

---

## Summary table

| Use `.env`? | Required? | Where?   | Commit to Git? | Loader         |
|:-----------:|:---------:|:--------:|:--------------:|:---------------|
| Recommended | No        | Project root | **No**          | python-dotenv   |

---

For more, see [python-dotenv documentation](https://pypi.org/project/python-dotenv/).
