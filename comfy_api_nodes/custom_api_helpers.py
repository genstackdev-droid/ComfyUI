"""
Helper functions for using custom API configurations with ComfyUI API nodes.

This module provides utilities to automatically configure API operations
with custom endpoints and API keys based on the provider.
"""

from typing import Optional, Dict, Any
from comfy.cli_args import args
from comfy_api_nodes.custom_api_config import get_config


def get_provider_from_path(path: str) -> Optional[str]:
    """
    Extract provider name from API path.
    
    Args:
        path: API endpoint path (e.g., "/proxy/openai/images/generations")
        
    Returns:
        Provider name or None if not found
    """
    # Remove leading slash and split
    parts = path.lstrip('/').split('/')
    
    # Common patterns:
    # /proxy/{provider}/...
    # /{provider}/...
    if len(parts) >= 2:
        if parts[0] == 'proxy':
            return parts[1].lower()
        else:
            return parts[0].lower()
    
    return None


def get_custom_api_base(provider: Optional[str], default: Optional[str] = None) -> str:
    """
    Get the API base URL for a provider, considering custom configuration.
    
    Args:
        provider: Provider name (e.g., "openai", "stability")
        default: Default URL if no custom URL is configured
        
    Returns:
        API base URL to use
    """
    config = get_config()
    
    # If provider specified and has custom config, use it
    if provider:
        custom_url = config.get_base_url(provider)
        if custom_url:
            return custom_url
    
    # Fall back to default or comfy_api_base
    return default or args.comfy_api_base


def get_custom_api_key(provider: Optional[str], auth_kwargs: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """
    Get the API key for a provider from custom configuration.
    
    Args:
        provider: Provider name (e.g., "openai", "stability")
        auth_kwargs: Existing auth kwargs dict
        
    Returns:
        API key or None
    """
    config = get_config()
    
    if provider:
        custom_key = config.get_api_key(provider)
        if custom_key:
            return custom_key
    
    # Fall back to existing auth_kwargs
    if auth_kwargs:
        return auth_kwargs.get("comfy_api_key") or auth_kwargs.get("auth_token")
    
    return None


def apply_custom_config(
    provider: Optional[str],
    api_base: Optional[str] = None,
    auth_kwargs: Optional[Dict[str, Any]] = None,
    path: Optional[str] = None
) -> tuple[str, Dict[str, Any]]:
    """
    Apply custom configuration to API operation parameters.
    
    Args:
        provider: Provider name (if known)
        api_base: Current API base URL
        auth_kwargs: Current auth kwargs
        path: API endpoint path (used to detect provider if not specified)
        
    Returns:
        Tuple of (api_base, auth_kwargs) with custom configuration applied
    """
    # Try to detect provider from path if not provided
    if not provider and path:
        provider = get_provider_from_path(path)
    
    # Get custom API base
    final_api_base = get_custom_api_base(provider, api_base)
    
    # Get custom API key
    custom_key = get_custom_api_key(provider, auth_kwargs)
    
    # Prepare auth_kwargs
    final_auth_kwargs = auth_kwargs.copy() if auth_kwargs else {}
    if custom_key:
        # Determine which key field to use based on the key format
        if custom_key.startswith('Bearer '):
            final_auth_kwargs['auth_token'] = custom_key.replace('Bearer ', '')
        else:
            final_auth_kwargs['comfy_api_key'] = custom_key
    
    return final_api_base, final_auth_kwargs


def transform_path_for_custom_api(path: str, provider: Optional[str] = None) -> str:
    """
    Transform a ComfyUI proxy path to work with custom API endpoints.
    
    When using custom APIs, we typically don't want the /proxy/{provider} prefix.
    This function removes it if a custom API is configured.
    
    Args:
        path: Original API path (e.g., "/proxy/openai/v1/images/generations")
        provider: Provider name (if known)
        
    Returns:
        Transformed path suitable for the configured endpoint
    """
    # Detect provider if not provided
    if not provider:
        provider = get_provider_from_path(path)
    
    config = get_config()
    
    # If using custom API, remove /proxy/{provider} prefix
    if provider and config.is_custom_configured(provider):
        parts = path.lstrip('/').split('/')
        if len(parts) >= 2 and parts[0] == 'proxy' and parts[1].lower() == provider.lower():
            # Remove /proxy/{provider} and return the rest
            remaining = '/'.join(parts[2:])
            return f"/{remaining}" if remaining else "/"
    
    # Return original path if not using custom API
    return path
