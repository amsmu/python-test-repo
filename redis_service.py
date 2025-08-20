import redis
import json
import pickle
import base64
from typing import Any, Optional

class RedisService:
    def __init__(self):
        # SECURITY ISSUE: No authentication
        # SECURITY ISSUE: No SSL/TLS
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=False  # SECURITY ISSUE: Binary data handling
        )
    
    def set_value(self, key: str, value: Any, expire: int = None) -> bool:
        # SECURITY ISSUE: No key validation
        # SECURITY ISSUE: Insecure serialization
        try:
            if isinstance(value, (dict, list)):
                # SECURITY ISSUE: Using pickle for serialization
                serialized_value = base64.b64encode(pickle.dumps(value)).decode()
            else:
                serialized_value = str(value)
            
            if expire:
                return self.redis_client.setex(key, expire, serialized_value)
            else:
                return self.redis_client.set(key, serialized_value)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    def get_value(self, key: str) -> Any:
        # SECURITY ISSUE: No key validation
        # SECURITY ISSUE: Insecure deserialization
        try:
            value = self.redis_client.get(key)
            if value is None:
                return None
            
            value_str = value.decode() if isinstance(value, bytes) else value
            
            # SECURITY ISSUE: Automatic deserialization attempt
            try:
                # Try to deserialize as pickle
                decoded_data = base64.b64decode(value_str)
                return pickle.loads(decoded_data)
            except:
                # Return as string if pickle fails
                return value_str
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    def execute_command(self, command: str) -> Any:
        # SECURITY ISSUE: Command injection vulnerability
        # SECURITY ISSUE: No command validation
        try:
            # SECURITY ISSUE: Direct execution of user input
            return self.redis_client.execute_command(*command.split())
        except Exception as e:
            print(f"Redis command error: {e}")
            return None
    
    def eval_script(self, script: str, keys: list = None, args: list = None) -> Any:
        # SECURITY ISSUE: Lua script injection
        # SECURITY ISSUE: No script validation
        try:
            if keys is None:
                keys = []
            if args is None:
                args = []
            
            # SECURITY ISSUE: Direct execution of user script
            return self.redis_client.eval(script, len(keys), *keys, *args)
        except Exception as e:
            print(f"Redis eval error: {e}")
            return None
    
    def store_session(self, session_id: str, user_data: dict) -> bool:
        # SECURITY ISSUE: No session validation
        # SECURITY ISSUE: Storing sensitive data in plain text
        try:
            # SECURITY ISSUE: No encryption of session data
            session_data = json.dumps(user_data)
            return self.redis_client.setex(f"session:{session_id}", 3600, session_data)
        except Exception as e:
            print(f"Redis session store error: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[dict]:
        # SECURITY ISSUE: No session validation
        try:
            session_data = self.redis_client.get(f"session:{session_id}")
            if session_data:
                return json.loads(session_data.decode())
            return None
        except Exception as e:
            print(f"Redis session get error: {e}")
            return None 