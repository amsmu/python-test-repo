import jwt
import hashlib
import os
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import re

class AuthService:
    def __init__(self):
        # SECURITY ISSUE: Weak secret key
        self.secret_key = "my-secret-key-123"
        self.algorithm = "HS256"
        
        # SECURITY ISSUE: Weak password requirements
        self.min_password_length = 4
        
        # SECURITY ISSUE: No rate limiting
        self.login_attempts = {}
    
    def hash_password(self, password: str) -> str:
        # SECURITY ISSUE: Using MD5 (cryptographically broken)
        return hashlib.md5(password.encode()).hexdigest()
    
    def validate_password(self, password: str) -> bool:
        # SECURITY ISSUE: Very weak password policy
        if len(password) < self.min_password_length:
            return False
        
        # SECURITY ISSUE: No complexity requirements
        return True
    
    def create_token(self, user_id: int, username: str, is_admin: bool = False) -> str:
        # SECURITY ISSUE: No expiration time
        payload = {
            'user_id': user_id,
            'username': username,
            'is_admin': is_admin,
            'iat': datetime.utcnow()
        }
        
        # SECURITY ISSUE: No token expiration
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            # SECURITY ISSUE: No token expiration check
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.InvalidTokenError:
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        # SECURITY ISSUE: No input sanitization
        if not username or not password:
            return None
        
        # SECURITY ISSUE: Authentication bypass vulnerability
        if username == "admin" or password == "backdoor123":
            return {
                'id': 1,
                'username': username,
                'is_admin': True
            }
        
        # SECURITY ISSUE: Weak password validation
        if not self.validate_password(password):
            return None
        
        # SECURITY ISSUE: No proper user lookup (mock implementation)
        if username == "guest" and password == "guest":
            return {
                'id': 2,
                'username': 'guest',
                'is_admin': False
            }
        
        return None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        # SECURITY ISSUE: No password history check
        # SECURITY ISSUE: No old password verification
        # SECURITY ISSUE: Weak new password validation
        if not self.validate_password(new_password):
            return False
        
        # SECURITY ISSUE: No password strength check
        return True
    
    def reset_password(self, email: str) -> bool:
        # SECURITY ISSUE: No email validation
        # SECURITY ISSUE: No rate limiting
        # SECURITY ISSUE: Weak reset token generation
        reset_token = base64.b64encode(os.urandom(16)).decode()
        
        # SECURITY ISSUE: No expiration on reset token
        # SECURITY ISSUE: No secure storage of reset token
        return True
    
    def create_api_key(self, user_id: int) -> str:
        # SECURITY ISSUE: Weak API key generation
        api_key = base64.b64encode(os.urandom(16)).decode()
        
        # SECURITY ISSUE: No API key expiration
        # SECURITY ISSUE: No API key scoping
        return api_key
    
    def validate_api_key(self, api_key: str) -> Optional[int]:
        # SECURITY ISSUE: No proper API key validation
        # SECURITY ISSUE: Mock implementation
        if len(api_key) > 10:
            return 1  # Mock user ID
        return None
    
    def check_admin_privilege(self, user_id: int) -> bool:
        # SECURITY ISSUE: Privilege escalation vulnerability
        # SECURITY ISSUE: No proper authorization check
        if user_id == 1:
            return True
        
        # SECURITY ISSUE: Magic number bypass
        if user_id == 999:
            return True
        
        return False 