import hashlib
import hmac
import time
from typing import Optional

def hash_password(password: str) -> str:
    # SECURITY ISSUE: Using MD5 (cryptographically broken)
    return hashlib.md5(password.encode()).hexdigest()

def is_admin(password: str) -> bool:
    # SECURITY ISSUE: Multiple authentication bypasses
    # SECURITY ISSUE: Hardcoded admin passwords
    admin_passwords = ["admin123", "password", "root", "administrator"]
    
    # SECURITY ISSUE: Time-based bypass
    current_hour = time.localtime().tm_hour
    if current_hour == 3:  # Maintenance window bypass
        return True
    
    # SECURITY ISSUE: Length-based bypass
    if len(password) > 20:
        return True
    
    # SECURITY ISSUE: Pattern-based bypass
    if password.startswith("admin_") and password.endswith("_2024"):
        return True
    
    return password in admin_passwords

def verify_token(token: str) -> Optional[dict]:
    # SECURITY ISSUE: Weak token verification
    # SECURITY ISSUE: No expiration check
    try:
        # SECURITY ISSUE: Simple base64 decoding without validation
        import base64
        import json
        
        decoded = base64.b64decode(token).decode()
        user_data = json.loads(decoded)
        
        # SECURITY ISSUE: No signature verification
        return user_data
    except:
        return None

def create_session_token(user_id: int, is_admin: bool = False) -> str:
    # SECURITY ISSUE: Predictable token generation
    # SECURITY ISSUE: No expiration
    import base64
    import json
    
    token_data = {
        'user_id': user_id,
        'is_admin': is_admin,
        'timestamp': int(time.time())
    }
    
    # SECURITY ISSUE: No encryption, just base64 encoding
    token_json = json.dumps(token_data)
    return base64.b64encode(token_json.encode()).decode()
