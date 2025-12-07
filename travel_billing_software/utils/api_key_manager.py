"""
API Key Manager - Secure storage for AI API keys
Uses base64 encoding for basic obfuscation
"""
import os
import json
import base64
from pathlib import Path

# Define path for API key storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY_FILE = os.path.join(BASE_DIR, "config", ".api_keys.json")


class APIKeyManager:
    """Manages secure storage and retrieval of API keys."""
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APIKeyManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the API key storage."""
        self.keys = {}
        self._load_keys()

    def _encode_key(self, key: str) -> str:
        """Encode API key using base64 for basic obfuscation."""
        if not key:
            return ""
        return base64.b64encode(key.encode()).decode()

    def _decode_key(self, encoded_key: str) -> str:
        """Decode API key from base64."""
        if not encoded_key:
            return ""
        try:
            return base64.b64decode(encoded_key.encode()).decode()
        except Exception:
            return ""

    def _load_keys(self):
        """Load API keys from storage file."""
        if os.path.exists(API_KEY_FILE):
            try:
                with open(API_KEY_FILE, 'r', encoding='utf-8') as f:
                    encoded_data = json.load(f)
                    # Decode all keys
                    self.keys = {
                        name: self._decode_key(encoded_key)
                        for name, encoded_key in encoded_data.items()
                    }
            except Exception as e:
                print(f"Error loading API keys: {e}")
                self.keys = {}
        else:
            self.keys = {}

    def _save_keys(self):
        """Save API keys to storage file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(API_KEY_FILE), exist_ok=True)
            
            # Encode all keys before saving
            encoded_data = {
                name: self._encode_key(key)
                for name, key in self.keys.items()
            }
            
            with open(API_KEY_FILE, 'w', encoding='utf-8') as f:
                json.dump(encoded_data, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving API keys: {e}")
            return False

    def set_api_key(self, key_name: str, api_key: str) -> bool:
        """
        Store an API key securely.
        
        Args:
            key_name: Name identifier for the key (e.g., 'google_ai', 'openai')
            api_key: The actual API key to store
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.keys[key_name] = api_key
            return self._save_keys()
        except Exception as e:
            print(f"Error setting API key: {e}")
            return False

    def get_api_key(self, key_name: str) -> str:
        """
        Retrieve an API key.
        
        Args:
            key_name: Name identifier for the key
            
        Returns:
            str: The API key, or empty string if not found
        """
        return self.keys.get(key_name, "")

    def delete_api_key(self, key_name: str) -> bool:
        """
        Delete an API key.
        
        Args:
            key_name: Name identifier for the key
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if key_name in self.keys:
                del self.keys[key_name]
                return self._save_keys()
            return False
        except Exception as e:
            print(f"Error deleting API key: {e}")
            return False

    def has_api_key(self, key_name: str) -> bool:
        """
        Check if an API key exists.
        
        Args:
            key_name: Name identifier for the key
            
        Returns:
            bool: True if key exists and is not empty
        """
        return bool(self.keys.get(key_name, ""))


# Singleton instance
def get_api_key_manager():
    """Get the singleton instance of APIKeyManager."""
    return APIKeyManager()
