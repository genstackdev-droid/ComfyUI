# Custom API Configuration for ComfyUI API Nodes

This guide explains how to configure ComfyUI API nodes to use your own custom API endpoints instead of the default ComfyUI API.

## Overview

By default, all API nodes in ComfyUI use the ComfyUI API (https://api.comfy.org) as a proxy to various AI service providers. However, you may want to:

- Use your own API keys directly with providers (OpenAI, Stability AI, etc.)
- Route requests through your own proxy server
- Use alternative or custom implementations of these APIs
- Have more control over API costs and usage

This custom API configuration system allows you to do all of that!

## Features

- ✅ Configure custom API endpoints per provider
- ✅ Use your own API keys
- ✅ Configuration via JSON file or environment variables
- ✅ Automatic path transformation for custom APIs
- ✅ Backward compatible with existing ComfyUI API
- ✅ Per-provider configuration flexibility

## Quick Start

### Method 1: JSON Configuration File

1. Copy the example configuration file:
   ```bash
   cp comfy_api_nodes/custom_api_config.json.example comfy_api_nodes/custom_api_config.json
   ```

2. Edit `custom_api_config.json` with your custom settings:
   ```json
   {
     "openai": {
       "base_url": "https://api.openai.com/v1",
       "api_key": "sk-your-openai-api-key-here"
     },
     "stability": {
       "base_url": "https://api.stability.ai",
       "api_key": "your-stability-api-key"
     }
   }
   ```

3. Start ComfyUI normally - the custom configuration will be automatically loaded!

### Method 2: Environment Variables

Set environment variables for each provider you want to customize:

```bash
# For OpenAI
export COMFY_API_OPENAI_BASE_URL="https://api.openai.com/v1"
export COMFY_API_OPENAI_API_KEY="sk-your-openai-api-key-here"

# For Stability AI
export COMFY_API_STABILITY_BASE_URL="https://api.stability.ai"
export COMFY_API_STABILITY_API_KEY="your-stability-api-key"

# Start ComfyUI
python main.py
```

Environment variables take precedence over JSON configuration.

## Supported Providers

The following providers can be configured:

- `openai` - OpenAI (DALL-E, GPT models)
- `stability` - Stability AI (Stable Diffusion, etc.)
- `bfl` - Black Forest Labs
- `runway` - Runway ML
- `luma` - Luma AI
- `pika` - Pika Labs
- `gemini` - Google Gemini
- `ideogram` - Ideogram
- `kling` - Kling AI
- `ltxv` - LTXV
- `minimax` - MiniMax
- `moonvalley` - Moonvalley
- `pixverse` - Pixverse
- `recraft` - Recraft
- `rodin` - Rodin
- `sora` - OpenAI Sora
- `tripo` - Tripo AI
- `veo2` - Google Veo 2
- `vidu` - Vidu
- `wan` - WAN
- `bytedance` - ByteDance

## Configuration Options

For each provider, you can configure:

### `base_url` (string)
The base URL for the API endpoint. This is the root URL that will be used for all API calls to this provider.

**Examples:**
- OpenAI: `https://api.openai.com/v1`
- Stability AI: `https://api.stability.ai`
- Custom proxy: `https://your-proxy.example.com/api`

### `api_key` (string)
Your API key for authenticating with the provider. This will be automatically included in API requests.

**Important:** Keep your API keys secure! Don't commit them to version control.

## How It Works

### Path Transformation

When using the ComfyUI API, paths typically look like:
```
/proxy/openai/v1/images/generations
```

When you configure a custom API, the system automatically transforms this to:
```
/v1/images/generations
```

This removes the `/proxy/{provider}` prefix so the path works correctly with the actual provider API.

### Authentication

Custom API keys are automatically injected into requests. The system determines the appropriate authentication method (Bearer token or API key header) based on the provider.

## Example Configurations

### Using OpenAI Directly

```json
{
  "openai": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-proj-..."
  }
}
```

### Using Azure OpenAI

```json
{
  "openai": {
    "base_url": "https://your-resource.openai.azure.com/openai/deployments/your-deployment",
    "api_key": "your-azure-api-key"
  }
}
```

### Using a Custom Proxy

If you have your own proxy that mimics the provider's API:

```json
{
  "stability": {
    "base_url": "https://my-proxy.example.com/stability",
    "api_key": "my-custom-key"
  }
}
```

### Mixed Configuration

You can use ComfyUI API for some providers and custom APIs for others:

```json
{
  "openai": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-..."
  }
  // stability, runway, etc. will still use ComfyUI API
}
```

## Modified Files

The following files have been modified to support custom API configuration:

### Core Files
- `comfy_api_nodes/custom_api_config.py` - Configuration manager
- `comfy_api_nodes/custom_api_helpers.py` - Helper functions for applying custom config
- `comfy_api_nodes/custom_api_config.json.example` - Example configuration file

### Modified Node Files
- `comfy_api_nodes/nodes_openai.py` - OpenAI nodes
- *(More node files can be modified using the same pattern)*

### Backup Directory
- `custom_api_nodes/` - Contains copies of all modified node files

## Modifying Additional Node Files

To modify additional API node files to support custom configuration, follow this pattern:

1. **Add the import:**
   ```python
   from comfy_api_nodes.custom_api_helpers import apply_custom_config, transform_path_for_custom_api
   ```

2. **Before creating an operation, apply custom config:**
   ```python
   # Apply custom API configuration
   path = "/proxy/provider/endpoint"
   custom_api_base, custom_auth_kwargs = apply_custom_config(
       provider="provider_name",
       auth_kwargs=kwargs,
       path=path
   )
   custom_path = transform_path_for_custom_api(path, provider="provider_name")
   ```

3. **Use custom config in the operation:**
   ```python
   operation = SynchronousOperation(
       endpoint=ApiEndpoint(
           path=custom_path,  # Use transformed path
           method=HttpMethod.POST,
           request_model=RequestModel,
           response_model=ResponseModel,
       ),
       request=RequestModel(...),
       api_base=custom_api_base,  # Add this
       auth_kwargs=custom_auth_kwargs,  # Use this instead of kwargs
   )
   ```

## Security Best Practices

1. **Never commit API keys to version control**
   - Add `custom_api_config.json` to `.gitignore`
   - Use environment variables in production

2. **Rotate API keys regularly**
   - Update your configuration when you rotate keys

3. **Use least privilege**
   - Only give API keys the minimum permissions needed

4. **Monitor usage**
   - Keep track of API usage and costs
   - Set up alerts for unusual activity

## Troubleshooting

### "Configuration file not found" Warning
This is normal if you haven't created `custom_api_config.json` yet. You can either:
- Create the file with your configuration
- Use environment variables instead
- Ignore the warning if using default ComfyUI API

### "API Error: Unauthorized"
Check that:
- Your API key is correct
- The API key has the necessary permissions
- The base URL is correct for your provider

### "Path not found" or 404 Errors
This usually means:
- The base URL is incorrect
- The path transformation isn't working correctly
- The provider's API structure differs from expected

Try checking the provider's API documentation and adjusting your base URL.

### Using Both ComfyUI API and Custom APIs
You can mix and match! Just configure the providers you want to customize and leave others unconfigured. Unconfigured providers will continue using the ComfyUI API.

## Need Help?

- Check the example configuration file: `custom_api_config.json.example`
- Review the provider's API documentation
- Test with a simple request first before using in complex workflows

## Advanced Usage

### Programmatic Configuration

You can also configure providers programmatically:

```python
from comfy_api_nodes.custom_api_config import get_config

config = get_config()
config.set_provider_config(
    provider="openai",
    base_url="https://api.openai.com/v1",
    api_key="sk-..."
)
config.save_config()
```

### Per-Request Configuration

For even more flexibility, you can pass custom `api_base` and `auth_kwargs` directly when creating operations in your custom nodes.

## Contributing

If you modify additional node files to support custom APIs:
1. Follow the pattern shown in this README
2. Test thoroughly with both ComfyUI API and custom APIs
3. Copy the modified file to `custom_api_nodes/` directory
4. Update this README with the node file name

## License

This configuration system is part of ComfyUI and follows the same license as the main project.
