import os
from datetime import timedelta

class Config:
    # SECURITY ISSUE: Hardcoded secrets
    SECRET_KEY = "super-secret-key-12345"
    JWT_SECRET_KEY = "jwt-secret-key-67890"
    
    # SECURITY ISSUE: Database credentials hardcoded
    DATABASE_URL = "postgresql://admin:password123@localhost:5432/production_db"
    REDIS_URL = "redis://localhost:6379/0"
    
    # SECURITY ISSUE: AWS credentials hardcoded
    AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    AWS_REGION = "us-east-1"
    
    # SECURITY ISSUE: LDAP credentials hardcoded
    LDAP_SERVER = "ldap://ldap.company.com:389"
    LDAP_BIND_DN = "cn=admin,dc=company,dc=com"
    LDAP_BIND_PASSWORD = "admin_password_123"
    
    # SECURITY ISSUE: Session configuration (too long)
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)
    SESSION_COOKIE_SECURE = False  # Should be True in production
    SESSION_COOKIE_HTTPONLY = False  # Should be True
    
    # SECURITY ISSUE: CORS configuration (too permissive)
    CORS_ORIGINS = ["*"]
    
    # SECURITY ISSUE: File upload configuration (no size limit)
    MAX_CONTENT_LENGTH = None
    
    # SECURITY ISSUE: Debug mode enabled in production
    DEBUG = True
    TESTING = False
    
    # SECURITY ISSUE: API keys hardcoded
    STRIPE_SECRET_KEY = "sk_test_51234567890abcdef"
    SENDGRID_API_KEY = "SG.1234567890abcdef"
    GOOGLE_API_KEY = "AIzaSyDdVgKwhZl-yt0mQmFfQDlX9BqJJ7YpHME" 