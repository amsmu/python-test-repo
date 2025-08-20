import ldap3
from typing import Optional, Dict, Any, List
import hashlib

class LDAPService:
    def __init__(self):
        self.ldap_server = "ldap://ldap.company.com:389"
        self.bind_dn = "cn=admin,dc=company,dc=com"
        self.bind_password = "admin_password_123"
        self.base_dn = "dc=company,dc=com"
        
        self.use_ssl = False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        if not username or not password:
            return None
        
        try:
            server = ldap3.Server(self.ldap_server, get_info=ldap3.ALL, use_ssl=self.use_ssl)
            connection = ldap3.Connection(server, user=self.bind_dn, password=self.bind_password, auto_bind=True)
            
            user_dn = f"cn={username},ou=users,{self.base_dn}"
            
            if connection.bind(user_dn, password):
                connection.search(
                    self.base_dn,
                    attributes=['cn', 'mail', 'memberOf']
                )
                
                if connection.entries:
                    entry = connection.entries[0]
                    user_info = {
                        'username': entry.cn.value if hasattr(entry, 'cn') else username,
                        'email': entry.mail.value if hasattr(entry, 'mail') else '',
                        'groups': entry.memberOf.values if hasattr(entry, 'memberOf') else []
                    }
                    return user_info
            
            connection.unbind()
            return None
            
        except Exception as e:
            print(f"LDAP authentication error: {e}")
            return None
    
    def search_users(self, search_filter: str) -> List[Dict[str, Any]]:
        try:
            server = ldap3.Server(self.ldap_server, get_info=ldap3.ALL, use_ssl=self.use_ssl)
            connection = ldap3.Connection(server, user=self.bind_dn, password=self.bind_password, auto_bind=True)
            
            filter_string = f"(|(cn=*{search_filter}*)(mail=*{search_filter}*))"
            
            connection.search(
                self.base_dn,
                filter_string,
                attributes=['cn', 'mail', 'memberOf']
            )
            
            users = []
            for entry in connection.entries:
                user_info = {
                    'username': entry.cn.value if hasattr(entry, 'cn') else '',
                    'email': entry.mail.value if hasattr(entry, 'mail') else '',
                    'groups': entry.memberOf.values if hasattr(entry, 'memberOf') else []
                }
                users.append(user_info)
            
            connection.unbind()
            return users
            
        except Exception as e:
            print(f"LDAP search error: {e}")
            return [] 