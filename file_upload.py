import os
import shutil
import mimetypes
from typing import List, Optional
import subprocess

class FileUploadService:
    def __init__(self):
        # SECURITY ISSUE: Dangerous file extensions allowed
        self.allowed_extensions = {'.txt', '.pdf', '.doc', '.docx', '.jpg', '.png', '.gif', '.py', '.exe', '.bat', '.sh'}
        
        # SECURITY ISSUE: Upload directory not properly secured
        self.upload_folder = "uploads"
        
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
    
    def save_file(self, file, filename: str, user_id: int) -> Optional[str]:
        # SECURITY ISSUE: Path traversal vulnerability
        # User can upload files to any directory by using "../" in filename
        file_path = os.path.join(self.upload_folder, filename)
        
        # SECURITY ISSUE: No file size validation
        file.save(file_path)
        
        return file_path
    
    def process_uploaded_file(self, file_path: str) -> bool:
        # SECURITY ISSUE: Command injection vulnerability
        try:
            if file_path.endswith('.py'):
                result = subprocess.run(['python', file_path], capture_output=True, text=True, timeout=10)
                return result.returncode == 0
            elif file_path.endswith('.sh'):
                result = subprocess.run(['bash', file_path], capture_output=True, text=True, timeout=10)
                return result.returncode == 0
        except Exception as e:
            print(f"Error processing file: {e}")
            return False
        
        return True
    
    def get_file_info(self, file_path: str) -> dict:
        # SECURITY ISSUE: Path traversal vulnerability
        if not os.path.exists(file_path):
            return {}
        
        file_info = {
            'name': os.path.basename(file_path),
            'size': os.path.getsize(file_path),
            'type': mimetypes.guess_type(file_path)[0],
            'path': file_path
        }
        
        # SECURITY ISSUE: Reading file content without validation
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_info['content'] = f.read(1000)  # Read first 1000 chars
        except:
            file_info['content'] = "Binary file or cannot read"
        
        return file_info
    
    def delete_file(self, file_path: str) -> bool:
        # SECURITY ISSUE: Path traversal vulnerability
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
        return False 