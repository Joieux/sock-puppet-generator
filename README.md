# 🧠 AI Sock Puppet Generator

An AI-driven agent that generates realistic sock puppet identities for authorized OSINT investigations, including fake names, AI-generated photos, bios, and Fastmail email aliases.

> ⚠️ For ethical and authorized use only (e.g., security research, threat intelligence).

---

## 🚀 Features

- AI-generated face images via [ThisPersonDoesNotExist](https://thispersondoesnotexist.com/)
- Fake names and background info via ElfQrin / Fake Name Generator
- Email alias creation (simulated Fastmail)
- Bio generation using OpenAI or local LLM (Ollama, LM Studio)
- TOR proxy support for anonymous scraping

---

## 🗂️ Project Structure

```
sockpuppet_agent/
├── main.py                  # Entry point
├── config.py                # API keys, LLM, proxy settings
├── agents/puppet_creator.py
├── utils/web_scrapers.py   # ElfQrin scraper
├── email/fastmail_api.py   # Alias mock/automation
├── requirements.txt
└── README.md
```

---

## 🔧 Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Tor (for proxy routing)
```bash
tor &  # or use system Tor service
```

### 3. Run the agent
```bash
python main.py
```

---

## ⚙️ Configuration (`config.py`)
Edit your API keys, proxy usage, and LLM endpoint inside `config.py`:
```python
CONFIG = {
    "openai_api_key": "sk-...",
    "use_local_llm": True,
    "local_llm_endpoint": "http://localhost:11434/api/generate",
    "use_tor_proxy": True,
    "tor_socks_proxy": "socks5h://127.0.0.1:9050"
}
```

---

## 🛡️ Legal & Ethical Use
This tool is for:
- Threat intelligence analysts
- Dark web researchers
- Red teamers with explicit legal authority

Never use this tool for impersonation, fraud, or violations of Terms of Service.

---

## 📌 Coming Soon
- Streamlit GUI
- Persona activity bot (Reddit, blogs)
- Real Fastmail browser automation (via Playwright)

---

## 📫 Contact
For collaboration or licensing questions: [Joieux] · [Your GitHub] 
