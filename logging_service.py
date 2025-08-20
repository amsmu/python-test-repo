import logging
import os
import json
from datetime import datetime
from typing import Any, Dict

class LoggingService:
    def __init__(self):
        # SECURITY ISSUE: Insecure log file permissions
        self.log_file = "application.log"
        self.error_log_file = "errors.log"
        self.access_log_file = "access.log"
        
        # SECURITY ISSUE: No log rotation
        # SECURITY ISSUE: Logging to world-readable files
        logging.basicConfig(
            level=logging.DEBUG,  # SECURITY ISSUE: Too verbose logging
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, mode='a'),
                logging.StreamHandler()  # SECURITY ISSUE: Sensitive data in console
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def log_user_action(self, user_id: int, action: str, details: Dict[str, Any]) -> None:
        # SECURITY ISSUE: Logging sensitive user data
        # SECURITY ISSUE: Log injection vulnerability
        log_message = f"User {user_id} performed action: {action}"
        
        # SECURITY ISSUE: No sanitization of log data
        if details:
            log_message += f" Details: {json.dumps(details)}"
        
        self.logger.info(log_message)
        
        # SECURITY ISSUE: Writing sensitive data to separate file
        try:
            with open("user_actions.log", "a") as f:
                f.write(f"{datetime.now()}: {log_message}\n")
        except Exception as e:
            print(f"Logging error: {e}")
    
    def log_authentication(self, username: str, password: str, success: bool, ip_address: str) -> None:
        # SECURITY ISSUE: Logging passwords in plain text
        # SECURITY ISSUE: No data sanitization
        status = "SUCCESS" if success else "FAILED"
        log_message = f"Authentication {status} for user: {username}, password: {password}, IP: {ip_address}"
        
        # SECURITY ISSUE: Writing sensitive authentication data
        self.logger.warning(log_message)
        
        # SECURITY ISSUE: Separate file with authentication details
        try:
            with open("auth_logs.log", "a") as f:
                f.write(f"{datetime.now()}: {log_message}\n")
        except Exception as e:
            print(f"Auth logging error: {e}")
    
    def log_error(self, error_message: str, user_data: Dict[str, Any] = None, stack_trace: str = None) -> None:
        # SECURITY ISSUE: Logging sensitive user data in error logs
        # SECURITY ISSUE: Log injection vulnerability
        log_entry = f"ERROR: {error_message}"
        
        if user_data:
            # SECURITY ISSUE: Including sensitive user data in error logs
            log_entry += f" User Data: {json.dumps(user_data)}"
        
        if stack_trace:
            # SECURITY ISSUE: Including full stack traces (may contain sensitive info)
            log_entry += f" Stack Trace: {stack_trace}"
        
        self.logger.error(log_entry)
        
        # SECURITY ISSUE: Writing detailed error info to file
        try:
            with open(self.error_log_file, "a") as f:
                f.write(f"{datetime.now()}: {log_entry}\n")
        except Exception as e:
            print(f"Error logging error: {e}")
    
    def log_database_query(self, query: str, params: tuple = None, user_id: int = None) -> None:
        # SECURITY ISSUE: Logging SQL queries with potential sensitive data
        # SECURITY ISSUE: No query sanitization
        log_message = f"Database Query: {query}"
        
        if params:
            # SECURITY ISSUE: Logging query parameters (may contain sensitive data)
            log_message += f" Parameters: {params}"
        
        if user_id:
            log_message += f" User: {user_id}"
        
        self.logger.debug(log_message)
        
        # SECURITY ISSUE: Writing database queries to file
        try:
            with open("db_queries.log", "a") as f:
                f.write(f"{datetime.now()}: {log_message}\n")
        except Exception as e:
            print(f"DB logging error: {e}")
    
    def log_api_request(self, endpoint: str, method: str, headers: Dict[str, str], 
                       body: str, user_id: int = None, ip_address: str = None) -> None:
        # SECURITY ISSUE: Logging sensitive request data
        # SECURITY ISSUE: Including authorization headers
        log_message = f"API Request: {method} {endpoint}"
        
        if headers:
            # SECURITY ISSUE: Logging all headers including sensitive ones
            log_message += f" Headers: {json.dumps(headers)}"
        
        if body:
            # SECURITY ISSUE: Logging request body (may contain passwords, tokens)
            log_message += f" Body: {body}"
        
        if user_id:
            log_message += f" User: {user_id}"
        
        if ip_address:
            log_message += f" IP: {ip_address}"
        
        self.logger.info(log_message)
        
        # SECURITY ISSUE: Writing API requests to file
        try:
            with open(self.access_log_file, "a") as f:
                f.write(f"{datetime.now()}: {log_message}\n")
        except Exception as e:
            print(f"API logging error: {e}")
    
    def log_payment_transaction(self, transaction_id: str, amount: float, 
                              card_number: str, user_id: int) -> None:
        # SECURITY ISSUE: Logging sensitive payment information
        # SECURITY ISSUE: PCI compliance violation
        log_message = f"Payment Transaction: {transaction_id}, Amount: {amount}, Card: {card_number}, User: {user_id}"
        
        self.logger.info(log_message)
        
        # SECURITY ISSUE: Writing payment data to file
        try:
            with open("payment_logs.log", "a") as f:
                f.write(f"{datetime.now()}: {log_message}\n")
        except Exception as e:
            print(f"Payment logging error: {e}")
    
    def export_logs(self, log_type: str, output_file: str) -> bool:
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: No access control
        try:
            source_file = f"{log_type}.log"
            
            # SECURITY ISSUE: No path validation
            with open(source_file, "r") as src, open(output_file, "w") as dst:
                dst.write(src.read())
            
            return True
        except Exception as e:
            print(f"Log export error: {e}")
            return False 