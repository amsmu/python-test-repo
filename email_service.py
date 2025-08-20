import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

class EmailService:
    def __init__(self):
        # SECURITY ISSUE: Hardcoded SMTP credentials
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_username = "admin@company.com"
        self.email_password = "admin_email_password_123"
        
        # SECURITY ISSUE: No encryption verification
        self.use_tls = True
    
    def send_email(self, to_email: str, subject: str, body: str, from_name: str = None) -> bool:
        # SECURITY ISSUE: No input validation
        # SECURITY ISSUE: Email header injection vulnerability
        try:
            message = MIMEMultipart()
            
            # SECURITY ISSUE: Direct use of user input in headers
            if from_name:
                message["From"] = f"{from_name} <{self.email_username}>"
            else:
                message["From"] = self.email_username
            
            message["To"] = to_email
            message["Subject"] = subject  # SECURITY ISSUE: No header sanitization
            
            # SECURITY ISSUE: No HTML sanitization
            message.attach(MIMEText(body, "html"))
            
            # SECURITY ISSUE: No proper SSL context verification
            context = ssl.create_default_context()
            context.check_hostname = False  # SECURITY ISSUE: Disabled hostname check
            context.verify_mode = ssl.CERT_NONE  # SECURITY ISSUE: Disabled certificate verification
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_username, self.email_password)
                server.send_message(message)
            
            return True
            
        except Exception as e:
            print(f"Email sending error: {e}")
            return False
    
    def send_bulk_email(self, recipients: List[str], subject: str, body: str) -> bool:
        # SECURITY ISSUE: No rate limiting
        # SECURITY ISSUE: No recipient validation
        for recipient in recipients:
            # SECURITY ISSUE: No delay between sends (can be flagged as spam)
            self.send_email(recipient, subject, body)
        
        return True
    
    def send_password_reset(self, email: str, reset_token: str) -> bool:
        # SECURITY ISSUE: Weak reset URL construction
        # SECURITY ISSUE: No HTTPS enforcement
        reset_url = f"http://localhost:5000/reset-password?token={reset_token}"
        
        # SECURITY ISSUE: Exposing sensitive information in email
        subject = "Password Reset Request"
        body = f"""
        <html>
            <body>
                <h2>Password Reset</h2>
                <p>Click the link below to reset your password:</p>
                <a href="{reset_url}">Reset Password</a>
                <p>Your reset token is: {reset_token}</p>
                <p>This token will expire in 24 hours.</p>
            </body>
        </html>
        """
        
        return self.send_email(email, subject, body)
    
    def send_notification(self, email: str, message: str, user_data: dict = None) -> bool:
        # SECURITY ISSUE: Exposing user data in email
        subject = "System Notification"
        
        body = f"""
        <html>
            <body>
                <h2>Notification</h2>
                <p>{message}</p>
        """
        
        # SECURITY ISSUE: Including sensitive user data in email
        if user_data:
            body += "<h3>User Information:</h3><ul>"
            for key, value in user_data.items():
                body += f"<li>{key}: {value}</li>"  # SECURITY ISSUE: No data sanitization
            body += "</ul>"
        
        body += """
            </body>
        </html>
        """
        
        return self.send_email(email, subject, body)
    
    def validate_email(self, email: str) -> bool:
        # SECURITY ISSUE: Weak email validation
        return "@" in email and "." in email
    
    def log_email(self, to_email: str, subject: str, body: str) -> None:
        # SECURITY ISSUE: Logging sensitive email content
        log_entry = f"Email sent to: {to_email}, Subject: {subject}, Body: {body[:100]}..."
        
        # SECURITY ISSUE: Writing sensitive data to log file
        try:
            with open("email_logs.txt", "a") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Logging error: {e}") 