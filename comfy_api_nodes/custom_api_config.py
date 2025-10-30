"""
Configuration module for custom API endpoints.

This module allows users to configure custom API endpoints for each provider
instead of using the default ComfyUI API endpoints.

Configuration can be provided via:
1. Environment variables (e.g., COMFY_API_OPENAI_BASE_URL)
2. A JSON configuration file (custom_api_config.json)
3. Programmatic configuration
"""

import os
import json
from typing import Optional, Dict
from pathlib import Path

# Default configuration file path
DEFAULT_CONFIG_FILE = Path(__file__).parent / "custom_api_config.json"

class CustomAPIConfig:
    """Configuration manager for custom API endpoints."""
    
    # Supported providers
    PROVIDERS = [
        "openai",
        "stability",
        "bfl",
        "bytedance",
        "gemini",
        "ideogram",
        "kling",
        "ltxv",
        "luma",
        "minimax",
        "moonvalley",
        "pika",
        "pixverse",
        "recraft",
        "rodin",
        "runway",
        "sora",
        "tripo",
        "veo2",
        "vidu",
        "wan",
    ]
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to custom configuration file. Defaults to custom_api_config.json
        """
        self.config_file = config_file or DEFAULT_CONFIG_FILE
        self._config: Dict[str, Dict[str, str]] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file and environment variables."""
        # First, try to load from JSON file
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self._config = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load custom API config from {self.config_file}: {e}")
        
        # Override with environment variables if present
        for provider in self.PROVIDERS:
            env_var_base = f"COMFY_API_{provider.upper()}_BASE_URL"
            env_var_key = f"COMFY_API_{provider.upper()}_API_KEY"
            
            if env_var_base in os.environ or env_var_key in os.environ:
                if provider not in self._config:
                    self._config[provider] = {}
                
                if env_var_base in os.environ:
                    self._config[provider]["base_url"] = os.environ[env_var_base]
                
                if env_var_key in os.environ:
                    self._config[provider]["api_key"] = os.environ[env_var_key]
    
    def get_base_url(self, provider: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get the custom base URL for a provider.
        
        Args:
            provider: Provider name (e.g., "openai", "stability")
            default: Default URL if no custom URL is configured
            
        Returns:
            Custom base URL or default URL
        """
        provider = provider.lower()
        if provider in self._config and "base_url" in self._config[provider]:
            return self._config[provider]["base_url"]
        return default
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """
        Get the custom API key for a provider.
        
        Args:
            provider: Provider name (e.g., "openai", "stability")
            
        Returns:
            Custom API key or None
        """
        provider = provider.lower()
        if provider in self._config and "api_key" in self._config[provider]:
            return self._config[provider]["api_key"]
        return None
    
    def set_provider_config(self, provider: str, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Set custom configuration for a provider.
        
        Args:
            provider: Provider name
            base_url: Custom base URL
            api_key: Custom API key
        """
        provider = provider.lower()
        if provider not in self._config:
            self._config[provider] = {}
        
        if base_url:
            self._config[provider]["base_url"] = base_url
        if api_key:
            self._config[provider]["api_key"] = api_key
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save custom API config to {self.config_file}: {e}")
    
    def is_custom_configured(self, provider: str) -> bool:
        """
        Check if a provider has custom configuration.
        
        Args:
            provider: Provider name
            
        Returns:
            True if custom configuration exists
        """
        provider = provider.lower()
        return provider in self._config and bool(self._config[provider])


# Global configuration instance
_config_instance: Optional[CustomAPIConfig] = None

def get_config() -> CustomAPIConfig:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = CustomAPIConfig()
    return _config_instance
