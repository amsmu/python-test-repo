import redis
import json
import pickle
import base64
from typing import Any, Optional

class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
        )
    
    def set_value(self, key: str, value: Any, expire: int = None) -> bool:
        try:
            if isinstance(value, (dict, list)):
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
        try:
            value = self.redis_client.get(key)
            if value is None:
                return None
            
            value_str = value.decode() if isinstance(value, bytes) else value
            
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
        try:
            return self.redis_client.execute_command(*command.split())
        except Exception as e:
            print(f"Redis command error: {e}")
            return None
    
    def eval_script(self, script: str, keys: list = None, args: list = None) -> Any:
        try:
            if keys is None:
                keys = []
            if args is None:
                args = []
            
            return self.redis_client.eval(script, len(keys), *keys, *args)
        except Exception as e:
            print(f"Redis eval error: {e}")
            return None
    
    def store_session(self, session_id: str, user_data: dict) -> bool:
        try:
            session_data = json.dumps(user_data)
            return self.redis_client.setex(f"session:{session_id}", 3600, session_data)
        except Exception as e:
            print(f"Redis session store error: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[dict]:
        try:
            session_data = self.redis_client.get(f"session:{session_id}")
            if session_data:
                return json.loads(session_data.decode())
            return None
        except Exception as e:
            print(f"Redis session get error: {e}")
            return None 