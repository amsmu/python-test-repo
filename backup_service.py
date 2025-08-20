import os
import shutil
import subprocess
import tarfile
import zipfile
from datetime import datetime
from typing import List, Optional

class BackupService:
    def __init__(self):
        # SECURITY ISSUE: Hardcoded backup paths
        self.backup_dir = "/tmp/backups"
        self.database_file = "users.db"
        
        # SECURITY ISSUE: No proper directory creation
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir, mode=0o777)  # SECURITY ISSUE: Too permissive
    
    def create_database_backup(self, backup_name: str) -> Optional[str]:
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: No input validation
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            # SECURITY ISSUE: No file existence check
            shutil.copy2(self.database_file, backup_path)
            return backup_path
        except Exception as e:
            print(f"Backup error: {e}")
            return None
    
    def restore_database(self, backup_file: str) -> bool:
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: No backup integrity check
        try:
            shutil.copy2(backup_file, self.database_file)
            return True
        except Exception as e:
            print(f"Restore error: {e}")
            return False
    
    def create_full_backup(self, directories: List[str], output_file: str) -> bool:
        # SECURITY ISSUE: Command injection vulnerability
        # SECURITY ISSUE: No input validation
        try:
            # SECURITY ISSUE: Using shell=True with user input
            command = f"tar -czf {output_file} " + " ".join(directories)
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Full backup error: {e}")
            return False
    
    def extract_backup(self, backup_file: str, extract_to: str) -> bool:
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: Zip slip vulnerability
        try:
            if backup_file.endswith('.tar.gz'):
                with tarfile.open(backup_file, 'r:gz') as tar:
                    # SECURITY ISSUE: No path validation during extraction
                    tar.extractall(path=extract_to)
            elif backup_file.endswith('.zip'):
                with zipfile.ZipFile(backup_file, 'r') as zip_ref:
                    # SECURITY ISSUE: No path validation during extraction
                    zip_ref.extractall(extract_to)
            
            return True
        except Exception as e:
            print(f"Extract error: {e}")
            return False
    
    def list_backups(self, directory: str = None) -> List[str]:
        # SECURITY ISSUE: Path traversal vulnerability
        if directory is None:
            directory = self.backup_dir
        
        try:
            # SECURITY ISSUE: No directory validation
            return os.listdir(directory)
        except Exception as e:
            print(f"List backups error: {e}")
            return []
    
    def delete_backup(self, backup_file: str) -> bool:
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: No access control
        try:
            if os.path.exists(backup_file):
                os.remove(backup_file)
                return True
        except Exception as e:
            print(f"Delete backup error: {e}")
        return False
    
    def compress_directory(self, source_dir: str, output_file: str) -> bool:
        # SECURITY ISSUE: Command injection vulnerability
        try:
            # SECURITY ISSUE: Direct command execution with user input
            command = f"zip -r {output_file} {source_dir}"
            result = subprocess.run(command, shell=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Compression error: {e}")
            return False 