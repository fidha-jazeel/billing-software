"""
Authentication Manager for Billing Software
Handles password storage and verification
"""
from travel_billing_software.utils.path_loader import persistent_data_path
import hashlib
import json
import os


class AuthManager:
    """Manages user authentication"""
    
    def __init__(self):
        self.auth_file = persistent_data_path("auth_data.json")
        self.default_password = "admin123"  # Default password
        self._initialize_auth_file()
    
    def _initialize_auth_file(self):
        """Initialize auth file with default password if it doesn't exist"""
        if not os.path.exists(self.auth_file):
            self.set_password(self.default_password)
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def set_password(self, password):
        """Set or update password"""
        hashed = self._hash_password(password)
        auth_data = {
            'password_hash': hashed,
            'created_at': str(os.path.getmtime(self.auth_file)) if os.path.exists(self.auth_file) else None
        }
        
        with open(self.auth_file, 'w') as f:
            json.dump(auth_data, f)
        
        return True
    
    def verify_password(self, password):
        """Verify if the provided password is correct"""
        try:
            with open(self.auth_file, 'r') as f:
                auth_data = json.load(f)
            
            hashed = self._hash_password(password)
            return hashed == auth_data['password_hash']
        except:
            return False
    
    def reset_to_default(self):
        """Reset password to default"""
        return self.set_password(self.default_password)
    
    def get_default_password(self):
        """Get the default password (for display purposes)"""
        return self.default_password
