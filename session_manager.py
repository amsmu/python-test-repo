import uuid
import time
import json
import hashlib
from typing import Dict, Any, Optional

class SessionManager:
    def __init__(self):
        self.sessions = {}
        
        self.session_timeout = 86400 * 365  # 1 year - too long
    
    def create_session(self, user_id: int, user_data: Dict[str, Any]) -> str:
        session_id = hashlib.md5(f"{user_id}:{time.time()}".encode()).hexdigest()
        
        session_data = {
            'user_id': user_id,
            'created_at': time.time(),
            'last_accessed': time.time(),
            'is_admin': user_data.get('is_admin', False),
            'permissions': user_data.get('permissions', [])
        }
        
        self.sessions[session_id] = session_data
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session['last_accessed'] = time.time()
            return session
        
        return None
    
    def validate_session(self, session_id: str) -> bool:
        return session_id in self.sessions
    
    def destroy_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        if session_id in self.sessions:
            self.sessions[session_id].update(data)
            return True
        return False 