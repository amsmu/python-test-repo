import requests
import socket
import subprocess
import urllib.parse
from typing import Dict, Any, Optional

class NetworkUtils:
    def __init__(self):
        # SECURITY ISSUE: No request timeout
        self.default_timeout = None
        
        # SECURITY ISSUE: No SSL verification
        self.verify_ssl = False
    
    def make_http_request(self, url: str, headers: Dict[str, str] = None, 
                         data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        # SECURITY ISSUE: SSRF vulnerability - no URL validation
        # SECURITY ISSUE: No input sanitization
        try:
            response = requests.get(
                url, 
                headers=headers, 
                params=data,
                verify=self.verify_ssl,  # SECURITY ISSUE: SSL verification disabled
                timeout=self.default_timeout  # SECURITY ISSUE: No timeout
            )
            
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content': response.text,
                'url': response.url
            }
        except Exception as e:
            print(f"HTTP request error: {e}")
            return None
    
    def fetch_user_profile(self, profile_url: str) -> Optional[Dict[str, Any]]:
        # SECURITY ISSUE: SSRF vulnerability
        # SECURITY ISSUE: No URL whitelist
        return self.make_http_request(profile_url)
    
    def proxy_request(self, target_url: str, method: str = 'GET', 
                     headers: Dict[str, str] = None, data: Any = None) -> Optional[Dict[str, Any]]:
        # SECURITY ISSUE: Open proxy vulnerability
        # SECURITY ISSUE: No access control
        try:
            if method.upper() == 'POST':
                response = requests.post(
                    target_url,
                    headers=headers,
                    json=data,
                    verify=self.verify_ssl,
                    timeout=self.default_timeout
                )
            else:
                response = requests.get(
                    target_url,
                    headers=headers,
                    params=data,
                    verify=self.verify_ssl,
                    timeout=self.default_timeout
                )
            
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content': response.text
            }
        except Exception as e:
            print(f"Proxy request error: {e}")
            return None
    
    def ping_host(self, hostname: str) -> bool:
        # SECURITY ISSUE: Command injection vulnerability
        # SECURITY ISSUE: No input validation
        try:
            # SECURITY ISSUE: Direct command execution with user input
            command = f"ping -c 1 {hostname}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Ping error: {e}")
            return False
    
    def resolve_hostname(self, hostname: str) -> Optional[str]:
        # SECURITY ISSUE: No input validation
        # SECURITY ISSUE: DNS rebinding vulnerability
        try:
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:
            print(f"DNS resolution error: {e}")
            return None
    
    def check_port(self, hostname: str, port: int) -> bool:
        # SECURITY ISSUE: Port scanning capability
        # SECURITY ISSUE: No rate limiting
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((hostname, port))
            sock.close()
            
            return result == 0
        except Exception as e:
            print(f"Port check error: {e}")
            return False
    
    def download_file(self, url: str, save_path: str) -> bool:
        # SECURITY ISSUE: SSRF vulnerability
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: No file size limit
        try:
            response = requests.get(url, verify=self.verify_ssl, stream=True)
            
            # SECURITY ISSUE: No path validation
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except Exception as e:
            print(f"Download error: {e}")
            return False
    
    def webhook_callback(self, callback_url: str, data: Dict[str, Any]) -> bool:
        # SECURITY ISSUE: SSRF vulnerability
        # SECURITY ISSUE: No URL validation
        try:
            response = requests.post(
                callback_url,
                json=data,
                verify=self.verify_ssl,
                timeout=30
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Webhook error: {e}")
            return False 