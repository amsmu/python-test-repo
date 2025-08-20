# Security Vulnerabilities Summary

This repository contains **20+ Python files** with **multiple sophisticated security vulnerabilities** for educational and testing purposes.

## Files Overview

### Core Application Files
1. **app.py** - Main Flask application with security misconfigurations
2. **config.py** - Configuration with hardcoded secrets
3. **models.py** - Database models with mass assignment vulnerabilities
4. **requirements.txt** - Dependencies with known vulnerabilities

### Authentication & Authorization
5. **auth.py** - Authentication with multiple bypass mechanisms
6. **auth_service.py** - Weak authentication service implementation
7. **session_manager.py** - Insecure session handling
8. **admin_panel.py** - Privilege escalation vulnerabilities

### Data Services
9. **database_service.py** - SQL injection vulnerabilities
10. **redis_service.py** - Insecure Redis operations with deserialization
11. **ldap_service.py** - LDAP injection vulnerabilities
12. **payment_service.py** - PCI compliance violations

### File & Network Operations
13. **file_upload.py** - Path traversal and execution vulnerabilities
14. **image_processor.py** - Command injection in image processing
15. **backup_service.py** - Path traversal and command injection
16. **network_utils.py** - SSRF and request forgery vulnerabilities

### API & Processing
17. **api_routes.py** - XSS, CSRF, and injection vulnerabilities
18. **xml_processor.py** - XXE and insecure deserialization
19. **crypto_service.py** - Weak cryptographic implementations
20. **email_service.py** - SMTP injection and credential exposure
21. **logging_service.py** - Sensitive data exposure in logs

## Major Vulnerability Categories

### 1. Injection Vulnerabilities
- **SQL Injection**: Direct query construction with user input
- **Command Injection**: Shell command execution with user data
- **LDAP Injection**: Unescaped LDAP filter construction
- **XXE Injection**: XML external entity processing
- **Template Injection**: Server-side template injection
- **XSS**: Cross-site scripting vulnerabilities

### 2. Authentication & Session Management
- **Weak Password Policies**: Minimal password requirements
- **Authentication Bypass**: Multiple bypass mechanisms
- **Session Fixation**: Predictable session IDs
- **Privilege Escalation**: Users can promote themselves to admin
- **Insecure Token Handling**: Base64 encoding without encryption

### 3. Sensitive Data Exposure
- **Hardcoded Credentials**: API keys, passwords, secrets in code
- **Information Disclosure**: Stack traces, environment variables
- **Logging Sensitive Data**: Passwords, credit cards in logs
- **PCI Violations**: Storing credit card data in plain text
- **Configuration Exposure**: Database credentials in responses

### 4. Security Misconfiguration
- **Debug Mode**: Enabled in production
- **CORS Misconfiguration**: Overly permissive origins
- **Missing Security Headers**: No CSRF, XSS protection
- **Insecure Permissions**: World-readable/writable files
- **SSL/TLS Issues**: Disabled certificate verification

### 5. Broken Access Control
- **Insecure Direct Object References**: Access any user's data
- **Missing Authorization**: No proper access controls
- **Path Traversal**: File system access outside intended directories
- **Mass Assignment**: Uncontrolled object property modification

### 6. Cryptographic Failures
- **Weak Algorithms**: MD5, SHA1 for password hashing
- **Hardcoded Keys**: Encryption keys in source code
- **Predictable Randomness**: Weak token/key generation
- **ECB Mode**: Insecure encryption modes
- **No Salt**: Password hashing without salt

### 7. Insecure Deserialization
- **Pickle Usage**: Insecure Python object serialization
- **No Validation**: Deserializing untrusted data
- **XML Deserialization**: Unsafe XML processing

### 8. Server-Side Request Forgery (SSRF)
- **Unvalidated URLs**: Making requests to arbitrary URLs
- **Internal Network Access**: Potential access to internal services
- **File System Access**: Reading local files via file:// URLs

### 9. File Upload Vulnerabilities
- **Unrestricted File Types**: Allowing executable files
- **Path Traversal**: Uploading to arbitrary locations
- **No Size Limits**: Potential DoS via large files
- **Execution**: Automatic processing of uploaded scripts

### 10. Business Logic Flaws
- **Race Conditions**: Concurrent access issues
- **Input Validation**: Missing or insufficient validation
- **State Management**: Improper workflow controls
- **Rate Limiting**: Missing API rate limits

## Example Exploits

### SQL Injection
```python
# In database_service.py
query = f"SELECT * FROM users WHERE username = '{username}'"
# Exploit: username = "admin' OR '1'='1' --"
```

### Authentication Bypass
```python
# In auth.py - Time-based bypass
if current_hour == 3:  # Maintenance window
    return True
# Exploit: Login at 3 AM for automatic admin access
```

### Command Injection
```python
# In network_utils.py
command = f"ping -c 1 {hostname}"
# Exploit: hostname = "google.com; rm -rf /"
```

### Path Traversal
```python
# In file_upload.py
file_path = os.path.join(self.upload_folder, filename)
# Exploit: filename = "../../etc/passwd"
```

## Disclaimer

⚠️ **WARNING**: This code contains intentional security vulnerabilities and should NEVER be used in production environments. It is designed for:

- Security testing and penetration testing practice
- Educational purposes to understand common vulnerabilities
- Security tool testing and validation
- Vulnerability research

**DO NOT** deploy this code in any production environment or expose it to the internet.

## Educational Value

This repository demonstrates real-world security vulnerabilities that are commonly found in production applications. Each vulnerability is clearly marked with comments explaining the security issue and potential impact.

Use this code to:
- Learn about common security vulnerabilities
- Practice identifying security issues
- Test security scanning tools
- Understand the impact of poor security practices
- Train development teams on secure coding practices 