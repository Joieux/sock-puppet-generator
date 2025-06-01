import random
import requests
from io import BytesIO
from typing import Optional, Dict, Any
import json
import time
import string

# Try to import utils, handle gracefully if missing
try:
    from utils.web_scrapers import get_fake_identity
    WEB_SCRAPERS_AVAILABLE = True
except ImportError:
    WEB_SCRAPERS_AVAILABLE = False
    # Create a fallback function
    def get_fake_identity():
        first_names = ["Alex", "Taylor", "Jordan", "Casey", "Morgan", "Riley", "Devon", "Sage"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        return {
            "name": f"{first_name} {last_name}",
            "first_name": first_name,
            "last_name": last_name,
            "username": f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}",
            "age": random.randint(18, 65),
            "gender": random.choice(["Male", "Female", "Non-binary"]),
            "phone": f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Elm', 'Park'])} St",
            "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
            "state": random.choice(["NY", "CA", "IL", "TX", "AZ"]),
            "zip_code": f"{random.randint(10000, 99999)}",
            "country": "United States",
            "occupation": random.choice(["Software Engineer", "Teacher", "Nurse", "Sales Rep", "Manager"])
        }

# Try to import mail utils, handle gracefully if missing
try:
    from mail_utils.fastmail_api import create_fastmail_alias
    MAIL_UTILS_AVAILABLE = True
except ImportError:
    MAIL_UTILS_AVAILABLE = False
    # Create a fallback function
    def create_fastmail_alias(base_name=None, domain="tempmail.org"):
        if not base_name:
            base_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        
        random_suffix = ''.join(random.choices(string.digits, k=4))
        email = f"{base_name}{random_suffix}@{domain}"
        
        return {
            "email": email,
            "alias": base_name,
            "domain": domain,
            "created": True,
            "status": "active"
        }

# Try to import config, handle gracefully if missing
try:
    from config import CONFIG
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    CONFIG = {
        "use_tor_proxy": False,
        "openai_api_key": "",
        "debug_mode": False
    }


def get_face_image() -> Optional[BytesIO]:
    """Generate or fetch a face image for the sock puppet"""
    try:
        # Use thispersondoesnotexist.com for AI-generated faces
        response = requests.get("https://thispersondoesnotexist.com/image", timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
    except Exception as e:
        print(f"Error fetching face image: {e}")
    
    return None


def generate_bio(identity_data: Dict[str, Any]) -> str:
    """Generate a simple biography for the sock puppet"""
    templates = [
        f"Hi! I'm {identity_data['first_name']}, a {identity_data['age']}-year-old {identity_data['occupation'].lower()} from {identity_data['city']}, {identity_data['state']}. I enjoy spending time with friends and exploring new technologies.",
        f"{identity_data['first_name']} here! Working as a {identity_data['occupation'].lower()} in {identity_data['city']}. Love connecting with new people and sharing experiences.",
        f"Hello, I'm {identity_data['first_name']} {identity_data['last_name']}. {identity_data['age']} years old and passionate about my work as a {identity_data['occupation'].lower()}. Based in {identity_data['city']}, {identity_data['state']}.",
    ]
    
    return random.choice(templates)


def generate_sock_puppet() -> Dict[str, Any]:
    """Generate a complete sock puppet identity"""
    
    try:
        # Get fake identity data
        identity = get_fake_identity()
        
        # Create email alias
        email_data = create_fastmail_alias(
            base_name=identity.get('username', '').lower(),
            domain="tempmail.org"
        )
        
        # Get profile image
        profile_image = get_face_image()
        
        # Generate bio
        bio = generate_bio(identity)
        
        # Combine all data
        puppet_data = {
            **identity,
            "email": email_data["email"],
            "email_alias": email_data,
            "profile_image": profile_image,
            "bio": bio,
            "created_timestamp": int(time.time()),
            "mail_utils_available": MAIL_UTILS_AVAILABLE,
            "web_scrapers_available": WEB_SCRAPERS_AVAILABLE,
            "config_available": CONFIG_AVAILABLE
        }
        
        return puppet_data
        
    except Exception as e:
        print(f"Error generating sock puppet: {e}")
        return None


def save_puppet_to_file(puppet_data: Dict[str, Any], filename: str = None) -> str:
    """Save puppet data to a JSON file"""
    if not filename:
        username = puppet_data.get('username', 'puppet')
        filename = f"{username}_puppet_data.json"
    
    try:
        # Remove non-serializable items
        serializable_data = {k: v for k, v in puppet_data.items() 
                           if k != 'profile_image'}
        
        with open(filename, 'w') as f:
            json.dump(serializable_data, f, indent=2)
        
        return filename
        
    except Exception as e:
        print(f"Error saving puppet data: {e}")
        return None


def get_puppet_summary(puppet_data: Dict[str, Any]) -> str:
    """Get a text summary of the puppet data"""
    if not puppet_data:
        return "No puppet data available"
    
    summary = f"""
Sock Puppet Identity Summary:
=============================
Name: {puppet_data.get('name', 'N/A')}
Username: {puppet_data.get('username', 'N/A')}
Email: {puppet_data.get('email', 'N/A')}
Age: {puppet_data.get('age', 'N/A')}
Location: {puppet_data.get('city', 'N/A')}, {puppet_data.get('state', 'N/A')}
Occupation: {puppet_data.get('occupation', 'N/A')}
Phone: {puppet_data.get('phone', 'N/A')}

Bio: {puppet_data.get('bio', 'N/A')}

Generated: {time.ctime(puppet_data.get('created_timestamp', time.time()))}
"""
    
    return summary


def validate_puppet_data(puppet_data: Dict[str, Any]) -> bool:
    """Validate that puppet data contains required fields"""
    required_fields = ['name', 'email', 'username']
    
    if not puppet_data:
        return False
    
    for field in required_fields:
        if field not in puppet_data or not puppet_data[field]:
            return False
    
    return True
