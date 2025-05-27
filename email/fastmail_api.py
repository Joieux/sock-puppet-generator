# sockpuppet_agent/email/fastmail_api.py
import requests
from config import CONFIG

def create_fastmail_alias(puppet_name):
    username = CONFIG["fastmail_username"]
    alias = puppet_name.lower().replace(" ", ".") + "@fastmail.com"
    return alias
