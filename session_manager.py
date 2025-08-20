import uuid
import time
import json
import hashlib
from typing import Dict, Any, Optional

class SessionManager:
    def __init__(self):
        # SECURITY ISSUE: In-memory storage (not persistent)
        self.sessions = {}
        
        # SECURITY ISSUE: Weak session configuration
        self.session_timeout = 86400 * 365  # 1 year - too long
        self.session_secret = "session-secret-123"  # SECURITY ISSUE: Hardcoded
    
    def create_session(self, user_id: int, user_data: Dict[str, Any]) -> str:
        # SECURITY ISSUE: Weak session ID generation
        session_id = hashlib.md5(f"{user_id}:{time.time()}".encode()).hexdigest()
        
        # SECURITY ISSUE: Storing sensitive data in session
        session_data = {
            'user_id': user_id,
            'created_at': time.time(),
            'last_accessed': time.time(),
            'user_data': user_data,  # SECURITY ISSUE: No data filtering
            'is_admin': user_data.get('is_admin', False),
            'permissions': user_data.get('permissions', [])
        }
        
        self.sessions[session_id] = session_data
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        # SECURITY ISSUE: No session validation
        # SECURITY ISSUE: No expiration check
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session['last_accessed'] = time.time()
            return session
        
        return None
    
    def validate_session(self, session_id: str) -> bool:
        # SECURITY ISSUE: Weak validation
        return session_id in self.sessions
    
    def destroy_session(self, session_id: str) -> bool:
        # SECURITY ISSUE: No proper cleanup
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        # SECURITY ISSUE: No input validation
        # SECURITY ISSUE: Can update any session data
        if session_id in self.sessions:
            self.sessions[session_id].update(data)
            return True
        return False 