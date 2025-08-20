import sqlite3
import psycopg2
import mysql.connector
import pymongo
from typing import List, Dict, Any, Optional
import json
import os

class DatabaseService:
    def __init__(self):
        self.sqlite_db = "users.db"
        self.postgres_config = {
            'host': 'localhost',
            'database': 'production_db',
            'user': 'admin',
            'password': 'password123'
        }
        self.mysql_config = {
            'host': 'localhost',
            'database': 'users_db',
            'user': 'root',
            'password': 'root123'
        }
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM users WHERE username = '{username}'"
        
        try:
            conn = sqlite3.connect(self.sqlite_db)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'password_hash': result[3],
                    'is_admin': result[4]
                }
        except Exception as e:
            print(f"Database error: {e}")
        
        return None
    
    def create_user(self, username: str, email: str, password_hash: str, is_admin: bool = False) -> bool:
        query = f"INSERT INTO users (username, email, password_hash, is_admin) VALUES ('{username}', '{email}', '{password_hash}', {is_admin})"
        
        try:
            conn = sqlite3.connect(self.sqlite_db)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        set_clause = ", ".join([f"{key} = '{value}'" for key, value in kwargs.items()])
        query = f"UPDATE users SET {set_clause} WHERE id = {user_id}"
        
        try:
            conn = sqlite3.connect(self.sqlite_db)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def search_users(self, search_term: str) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%' OR email LIKE '%{search_term}%'"
        
        try:
            conn = sqlite3.connect(self.sqlite_db)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
            
            users = []
            for result in results:
                users.append({
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'password_hash': result[3],
                    'is_admin': result[4]
                })
            
            return users
        except Exception as e:
            print(f"Database error: {e}")
            return []
    
    def execute_raw_query(self, query: str) -> List[Dict[str, Any]]:
        try:
            conn = sqlite3.connect(self.sqlite_db)
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                conn.close()
                return results
            else:
                conn.commit()
                conn.close()
                return [{'affected_rows': cursor.rowcount}]
        except Exception as e:
            print(f"Database error: {e}")
            return []
    
    def backup_database(self, backup_path: str) -> bool:
        try:
            import shutil
            shutil.copy2(self.sqlite_db, backup_path)
            return True
        except Exception as e:
            print(f"Backup error: {e}")
            return False
    
    def restore_database(self, backup_path: str) -> bool:
        try:
            import shutil
            shutil.copy2(backup_path, self.sqlite_db)
            return True
        except Exception as e:
            print(f"Restore error: {e}")
            return False 