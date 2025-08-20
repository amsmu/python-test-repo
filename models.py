from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    api_key = db.Column(db.String(255))
    ssn = db.Column(db.String(11))
    credit_card = db.Column(db.String(16))
    bank_account = db.Column(db.String(20))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'api_key': self.api_key,  # Should not expose
            'ssn': self.ssn,  # Should not expose
            'credit_card': self.credit_card,  # Should not expose
            'bank_account': self.bank_account  # Should not expose
        }

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    file_type = db.Column(db.String(50))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100))
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_agent = db.Column(db.Text)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(3), default='USD')
    
    credit_card_number = db.Column(db.String(16))
    cvv = db.Column(db.String(4))
    expiry_date = db.Column(db.String(5))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': float(self.amount),
            'currency': self.currency,
            'credit_card_number': self.credit_card_number,  # Should not expose
            'cvv': self.cvv,  # Should not expose
            'expiry_date': self.expiry_date  # Should not expose
        } 