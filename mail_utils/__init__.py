"""
FastMail API utilities for sock puppet generator
Provides email alias creation and management for OSINT research
"""
import random
import string
import requests
from typing import Optional, Dict, Any, List
import json
import time


def create_fastmail_alias(
    base_name: Optional[str] = None, 
    domain: str = "fastmail.com",
    use_random_domain: bool = True
) -> Dict[str, Any]:
    """
    Create a fake email alias for sock puppet generation.
    
    Args:
        base_name: Base name for the email (optional)
        domain: Email domain to use
        use_random_domain: Whether to use a random temporary email domain
        
    Returns:
        Dictionary containing email alias information
    """
    # Common temporary email domains for sock puppets
    temp_domains = [
        "tempmail.org",
        "guerrillamail.com", 
        "10minutemail.com",
        "mailinator.com",
        "temp-mail.org",
        "throwaway.email"
    ]
    
    if use_random_domain:
        domain = random.choice(temp_domains)
    
    if not base_name:
        # Generate realistic base name
        first_names = ["alex", "taylor", "jordan", "casey", "morgan", "riley", "devon", "sage"]
        last_names = ["smith", "johnson", "williams", "brown", "jones", "garcia", "miller", "davis"]
        base_name = f"{random.choice(first_names)}.{random.choice(last_names)}"
    
    # Generate random numbers for uniqueness
    random_suffix = ''.join(random.choices(string.digits, k=random.randint(2, 4)))
    
    email = f"{base_name}{random_suffix}@{domain}"
    
    return {
        "email": email,
        "alias": base_name,
        "domain": domain,
        "created": True,
        "status": "active",
        "created_at": int(time.time()),
        "service": "simulated_fastmail"
    }


def validate_email_alias(email: str) -> bool:
    """
    Validate an email alias format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid format, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def generate_multiple_aliases(count: int = 3, base_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Generate multiple email aliases for the same sock puppet.
    
    Args:
        count: Number of aliases to generate
        base_name: Base name to use for all aliases
        
    Returns:
        List of email alias dictionaries
    """
    aliases = []
    for i in range(count):
        alias_data = create_fastmail_alias(base_name=base_name)
        aliases.append(alias_data)
    
    return aliases


def delete_email_alias(email: str) -> Dict[str, Any]:
    """
    Mock function to delete an email alias.
    
    Args:
        email: Email address to delete
        
    Returns:
        Dictionary with deletion status
    """
    return {
        "email": email,
        "deleted": True,
        "status": "inactive",
        "deleted_at": int(time.time())
    }


def get_alias_info(email: str) -> Dict[str, Any]:
    """
    Get information about an email alias.
    
    Args:
        email: Email address to check
        
    Returns:
        Dictionary with alias information
    """
    return {
        "email": email,
        "valid": validate_email_alias(email),
        "domain": email.split("@")[-1] if "@" in email else None,
        "username": email.split("@")[0] if "@" in email else None,
        "status": "simulated"
    }


# For backwards compatibility
def create_temp_email(username: Optional[str] = None) -> str:
    """Create a temporary email address"""
    alias_data = create_fastmail_alias(base_name=username)
    return alias_data["email"]
