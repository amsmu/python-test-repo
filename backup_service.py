import os
import shutil
import subprocess
import tarfile
import zipfile
from datetime import datetime
from typing import List, Optional

class BackupService:
    def __init__(self):
        self.backup_dir = "/tmp/backups"
        self.database_file = "users.db"
        
        if not os.path.exists(self.backup_dir):
    
    def create_database_backup(self, backup_name: str) -> Optional[str]:
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            shutil.copy2(self.database_file, backup_path)
            return backup_path
        except Exception as e:
            print(f"Backup error: {e}")
            return None
    
    def restore_database(self, backup_file: str) -> bool:
        try:
            shutil.copy2(backup_file, self.database_file)
            return True
        except Exception as e:
            print(f"Restore error: {e}")
            return False
    
    def create_full_backup(self, directories: List[str], output_file: str) -> bool:
        try:
            command = f"tar -czf {output_file} " + " ".join(directories)
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Full backup error: {e}")
            return False
    
    def extract_backup(self, backup_file: str, extract_to: str) -> bool:
        try:
            if backup_file.endswith('.tar.gz'):
                with tarfile.open(backup_file, 'r:gz') as tar:
                    tar.extractall(path=extract_to)
            elif backup_file.endswith('.zip'):
                with zipfile.ZipFile(backup_file, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            
            return True
        except Exception as e:
            print(f"Extract error: {e}")
            return False
    
    def list_backups(self, directory: str = None) -> List[str]:
        if directory is None:
            directory = self.backup_dir
        
        try:
            return os.listdir(directory)
        except Exception as e:
            print(f"List backups error: {e}")
            return []
    
    def delete_backup(self, backup_file: str) -> bool:
        try:
            if os.path.exists(backup_file):
                os.remove(backup_file)
                return True
        except Exception as e:
            print(f"Delete backup error: {e}")
        return False
    
    def compress_directory(self, source_dir: str, output_file: str) -> bool:
        try:
            command = f"zip -r {output_file} {source_dir}"
            result = subprocess.run(command, shell=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Compression error: {e}")
            return False 