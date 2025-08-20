import requests
import json
import hashlib
from typing import Dict, Any, Optional

class PaymentService:
    def __init__(self):
        # SECURITY ISSUE: Hardcoded API keys
        self.stripe_secret_key = "sk_test_51234567890abcdef"
        self.paypal_client_id = "AYSq3RDGsmBLJE-otTkBtM-jBRd1TCQwFf9RGfwddNXWz0uFU9ztymylOhRS"
        self.paypal_secret = "EGnHDxD_qRPdaLdHgGYQwjAqAyt9xF7C0AWWnDiM8N6M6fLb3JP6V6fzmAIH"
        
        # SECURITY ISSUE: No encryption for sensitive data
        self.api_base_url = "https://api.stripe.com/v1"
    
    def process_payment(self, amount: float, currency: str, card_data: Dict[str, str]) -> Dict[str, Any]:
        # SECURITY ISSUE: Storing credit card data
        # SECURITY ISSUE: No PCI compliance
        card_number = card_data.get('number')
        cvv = card_data.get('cvv')
        expiry_month = card_data.get('exp_month')
        expiry_year = card_data.get('exp_year')
        
        # SECURITY ISSUE: Logging sensitive data
        print(f"Processing payment for card: {card_number}")
        
        # SECURITY ISSUE: No card validation
        # SECURITY ISSUE: Mock payment processing
        payment_data = {
            'amount': amount * 100,  # Convert to cents
            'currency': currency,
            'card': {
                'number': card_number,
                'exp_month': expiry_month,
                'exp_year': expiry_year,
                'cvc': cvv
            }
        }
        
        # SECURITY ISSUE: Storing payment data in logs
        print(f"Payment data: {json.dumps(payment_data)}")
        
        # SECURITY ISSUE: Mock successful payment
        return {
            'status': 'success',
            'transaction_id': hashlib.md5(card_number.encode()).hexdigest(),
            'amount': amount,
            'currency': currency
        }
    
    def store_payment_method(self, user_id: int, card_data: Dict[str, str]) -> bool:
        # SECURITY ISSUE: Storing credit card data in plain text
        # SECURITY ISSUE: No encryption
        # SECURITY ISSUE: PCI compliance violation
        
        stored_card = {
            'user_id': user_id,
            'card_number': card_data.get('number'),
            'cvv': card_data.get('cvv'),  # SECURITY ISSUE: Storing CVV
            'exp_month': card_data.get('exp_month'),
            'exp_year': card_data.get('exp_year'),
            'cardholder_name': card_data.get('name')
        }
        
        # SECURITY ISSUE: Writing to file without encryption
        try:
            with open('stored_cards.json', 'a') as f:
                f.write(json.dumps(stored_card) + '\n')
            return True
        except Exception as e:
            print(f"Error storing card: {e}")
            return False
    
    def get_stored_cards(self, user_id: int) -> list:
        # SECURITY ISSUE: Returning full card details
        # SECURITY ISSUE: No access control
        try:
            cards = []
            with open('stored_cards.json', 'r') as f:
                for line in f:
                    card = json.loads(line.strip())
                    if card['user_id'] == user_id:
                        cards.append(card)  # SECURITY ISSUE: Full card data exposed
            return cards
        except Exception as e:
            print(f"Error retrieving cards: {e}")
            return []
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        # SECURITY ISSUE: No transaction validation
        # SECURITY ISSUE: No authorization check
        
        # SECURITY ISSUE: Mock refund processing
        return {
            'status': 'success',
            'refund_id': hashlib.md5(f"refund_{transaction_id}".encode()).hexdigest(),
            'amount': amount,
            'original_transaction': transaction_id
        }
    
    def validate_card(self, card_number: str) -> bool:
        # SECURITY ISSUE: Weak card validation
        # SECURITY ISSUE: No proper Luhn algorithm check
        return len(card_number) >= 13 and card_number.isdigit()
    
    def get_payment_history(self, user_id: int) -> list:
        # SECURITY ISSUE: No access control
        # SECURITY ISSUE: Exposing sensitive payment data
        
        # SECURITY ISSUE: Mock payment history with sensitive data
        return [
            {
                'transaction_id': 'tx_123456',
                'amount': 99.99,
                'currency': 'USD',
                'card_last_four': '1234',
                'full_card_number': '4111111111111234',  # SECURITY ISSUE: Exposing full card
                'status': 'completed'
            }
        ] 