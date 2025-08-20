import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_username = "admin@company.com"
        self.email_password = "admin_email_password_123"
        
        self.use_tls = True
    
    def send_email(self, to_email: str, subject: str, body: str, from_name: str = None) -> bool:
        try:
            message = MIMEMultipart()
            
            if from_name:
                message["From"] = f"{from_name} <{self.email_username}>"
            else:
                message["From"] = self.email_username
            
            message["To"] = to_email
            
            message.attach(MIMEText(body, "html"))
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_username, self.email_password)
                server.send_message(message)
            
            return True
            
        except Exception as e:
            print(f"Email sending error: {e}")
            return False
    
    def send_bulk_email(self, recipients: List[str], subject: str, body: str) -> bool:
        for recipient in recipients:
            self.send_email(recipient, subject, body)
        
        return True
    
    def send_password_reset(self, email: str, reset_token: str) -> bool:
        reset_url = f"http://localhost:5000/reset-password?token={reset_token}"
        
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
        subject = "System Notification"
        
        body = f"""
        <html>
            <body>
                <h2>Notification</h2>
                <p>{message}</p>
        """
        
        if user_data:
            body += "<h3>User Information:</h3><ul>"
            for key, value in user_data.items():
            body += "</ul>"
        
        body += """
            </body>
        </html>
        """
        
        return self.send_email(email, subject, body)
    
    def validate_email(self, email: str) -> bool:
        return "@" in email and "." in email
    
    def log_email(self, to_email: str, subject: str, body: str) -> None:
        log_entry = f"Email sent to: {to_email}, Subject: {subject}, Body: {body[:100]}..."
        
        try:
            with open("email_logs.txt", "a") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Logging error: {e}") 