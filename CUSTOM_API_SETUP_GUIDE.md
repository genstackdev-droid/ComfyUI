# Custom API Setup Guide for ComfyUI

## What This Is

This modification allows you to use **your own API endpoints** with ComfyUI's API nodes instead of routing through ComfyUI's API server. This gives you:

- 🔑 **Direct API Access** - Use your own API keys with OpenAI, Stability AI, and other providers
- 💰 **Cost Control** - Manage your own API spending and billing
- 🔒 **Privacy** - Keep your requests between you and the provider
- 🌐 **Flexibility** - Use custom proxies or alternative API implementations
- ⚙️ **Per-Provider Configuration** - Mix and match; use ComfyUI API for some providers and your own for others

## Quick Start (5 Minutes)

### Step 1: Create Configuration File

```bash
cd /home/runner/work/ComfyUI/ComfyUI
cp comfy_api_nodes/custom_api_config.json.example comfy_api_nodes/custom_api_config.json
```

### Step 2: Add Your API Keys

Edit `comfy_api_nodes/custom_api_config.json`:

```json
{
  "openai": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-your-actual-openai-key-here"
  }
}
```

### Step 3: Start ComfyUI

```bash
python main.py
```

That's it! Your OpenAI nodes will now use your API key directly.

## What Was Modified

### New Files Created

1. **`comfy_api_nodes/custom_api_config.py`**
   - Configuration manager
   - Handles loading config from JSON and environment variables
   - Provides API to get custom URLs and keys per provider

2. **`comfy_api_nodes/custom_api_helpers.py`**
   - Helper functions for applying custom configuration
   - Automatic path transformation (removes `/proxy/{provider}` prefix)
   - Authentication handling

3. **`comfy_api_nodes/custom_api_config.json.example`**
   - Example configuration file
   - Shows format for all providers

4. **`comfy_api_nodes/CUSTOM_API_README.md`**
   - Detailed documentation
   - Examples and troubleshooting

5. **`comfy_api_nodes/apply_custom_api_to_node.py`**
   - Helper script to add custom API support to additional nodes
   - Adds TODO comments showing where to insert configuration code

6. **`comfy_api_nodes/apply_custom_api_to_all.sh`**
   - Batch script to process all API node files at once

### Modified Files

#### Fully Modified (Ready to Use)
- **`comfy_api_nodes/nodes_openai.py`** - All OpenAI operations now support custom APIs

#### Partially Modified (Needs Manual Completion)
All other node files have been prepared with TODO comments:
- `nodes_stability.py`
- `nodes_bfl.py`
- `nodes_runway.py`
- `nodes_luma.py`
- `nodes_pika.py`
- `nodes_gemini.py`
- And 13 more...

### Backup Directory
- **`custom_api_nodes/`** - Contains copies of all modified node files

## File Structure

```
ComfyUI/
├── comfy_api_nodes/
│   ├── custom_api_config.py          # New: Config manager
│   ├── custom_api_helpers.py         # New: Helper functions
│   ├── custom_api_config.json.example # New: Example config
│   ├── custom_api_config.json        # Your actual config (gitignored)
│   ├── CUSTOM_API_README.md          # New: Detailed docs
│   ├── apply_custom_api_to_node.py   # New: Helper script
│   ├── apply_custom_api_to_all.sh    # New: Batch processor
│   ├── nodes_openai.py               # Modified: Fully implemented
│   ├── nodes_stability.py            # Modified: Has TODO comments
│   └── [other node files...]         # Modified: Has TODO comments
├── custom_api_nodes/                 # New: Backup directory
│   └── [backup copies of modified files]
├── CUSTOM_API_SETUP_GUIDE.md         # This file
└── .gitignore                        # Updated: Ignores custom_api_config.json
```

## Configuration Methods

### Method 1: JSON File (Recommended)

Best for: Development, multiple providers, persistent configuration

```json
{
  "openai": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-..."
  },
  "stability": {
    "base_url": "https://api.stability.ai",
    "api_key": "sk-..."
  }
}
```

### Method 2: Environment Variables

Best for: Production, CI/CD, Docker deployments

```bash
export COMFY_API_OPENAI_BASE_URL="https://api.openai.com/v1"
export COMFY_API_OPENAI_API_KEY="sk-..."
export COMFY_API_STABILITY_BASE_URL="https://api.stability.ai"
export COMFY_API_STABILITY_API_KEY="sk-..."
python main.py
```

### Method 3: Programmatic

Best for: Custom integrations, dynamic configuration

```python
from comfy_api_nodes.custom_api_config import get_config

config = get_config()
config.set_provider_config(
    provider="openai",
    base_url="https://api.openai.com/v1",
    api_key="sk-..."
)
```

## Completing the Setup for Additional Providers

The OpenAI nodes are fully implemented and ready to use. For other providers, follow these steps:

### For Each Provider You Want to Use

1. **Find the TODO comments** in the node file:
   ```bash
   grep -n "TODO: Apply custom API configuration" comfy_api_nodes/nodes_stability.py
   ```

2. **Uncomment the configuration code:**
   ```python
   # Before (with TODO comment):
   # TODO: Apply custom API configuration
   # custom_api_base, custom_auth_kwargs = apply_custom_config(
   #     provider="stability",
   #     auth_kwargs=kwargs,
   #     path=path
   # )
   
   # After (uncommented and active):
   custom_api_base, custom_auth_kwargs = apply_custom_config(
       provider="stability",
       auth_kwargs=kwargs,
       path=path
   )
   custom_path = transform_path_for_custom_api(path, provider="stability")
   ```

3. **Update the operation parameters:**
   ```python
   # Change from:
   operation = SynchronousOperation(
       endpoint=ApiEndpoint(
           path=path,  # ← Change this
           ...
       ),
       auth_kwargs=kwargs,  # ← And this
   )
   
   # To:
   operation = SynchronousOperation(
       endpoint=ApiEndpoint(
           path=custom_path,  # ← Use transformed path
           ...
       ),
       api_base=custom_api_base,  # ← Add this
       auth_kwargs=custom_auth_kwargs,  # ← Use custom auth
   )
   ```

4. **Test it:**
   - Add the provider to your `custom_api_config.json`
   - Start ComfyUI
   - Test a workflow with that provider's nodes

## Supported Providers

| Provider | Modified | Status | Config Key |
|----------|----------|--------|------------|
| OpenAI | ✅ Fully | Ready to use | `openai` |
| Stability AI | ⚠️ Partial | Needs uncommenting | `stability` |
| Black Forest Labs | ⚠️ Partial | Needs uncommenting | `bfl` |
| Runway | ⚠️ Partial | Needs uncommenting | `runway` |
| Luma | ⚠️ Partial | Needs uncommenting | `luma` |
| Pika | ⚠️ Partial | Needs uncommenting | `pika` |
| Gemini | ⚠️ Partial | Needs uncommenting | `gemini` |
| Ideogram | ⚠️ Partial | Needs uncommenting | `ideogram` |
| Kling | ⚠️ Partial | Needs uncommenting | `kling` |
| LTXV | ⚠️ Partial | Needs uncommenting | `ltxv` |
| MiniMax | ⚠️ Partial | Needs uncommenting | `minimax` |
| Moonvalley | ⚠️ Partial | Needs uncommenting | `moonvalley` |
| Pixverse | ⚠️ Partial | Needs uncommenting | `pixverse` |
| Recraft | ⚠️ Partial | Needs uncommenting | `recraft` |
| Rodin | ⚠️ Partial | Needs uncommenting | `rodin` |
| Sora | ⚠️ Partial | Needs uncommenting | `sora` |
| Tripo | ⚠️ Partial | Needs uncommenting | `tripo` |
| Veo2 | ⚠️ Partial | Needs uncommenting | `veo2` |
| Vidu | ⚠️ Partial | Needs uncommenting | `vidu` |
| WAN | ⚠️ Partial | Needs uncommenting | `wan` |
| ByteDance | ⚠️ Partial | Needs uncommenting | `bytedance` |

## Example Configurations

### OpenAI Direct
```json
{
  "openai": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-proj-..."
  }
}
```

### Azure OpenAI
```json
{
  "openai": {
    "base_url": "https://your-resource.openai.azure.com/openai/deployments/your-deployment",
    "api_key": "your-azure-key"
  }
}
```

### Stability AI Direct
```json
{
  "stability": {
    "base_url": "https://api.stability.ai",
    "api_key": "sk-..."
  }
}
```

### Mixed Configuration
```json
{
  "openai": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-..."
  }
  // Other providers will use ComfyUI API
}
```

## Testing Your Setup

### 1. Verify Configuration Loads
```python
from comfy_api_nodes.custom_api_config import get_config

config = get_config()
print(config.is_custom_configured("openai"))  # Should print True
print(config.get_base_url("openai"))  # Should print your URL
```

### 2. Test with a Simple Workflow
- Create a workflow with an OpenAI DALL-E node
- Run the workflow
- Check logs for any authentication errors

### 3. Verify API Calls
- Monitor your API provider's dashboard
- Confirm requests are going directly to them (not through ComfyUI)

## Troubleshooting

### Configuration Not Loading
- Check file path: `comfy_api_nodes/custom_api_config.json`
- Verify JSON syntax is valid
- Check file permissions

### Unauthorized Errors
- Verify API key is correct
- Check if key has necessary permissions
- Ensure base URL is correct

### Path/404 Errors
- Check base URL format
- Verify path transformation is working
- Compare with provider's API documentation

### Still Using ComfyUI API
- Verify configuration is loaded: check startup logs
- Ensure provider name matches exactly
- Check if the node file has been fully modified (not just TODO comments)

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `custom_api_config.json` (it's gitignored)
- Rotate API keys regularly
- Use environment variables in production
- Monitor API usage for unusual activity
- Use least-privilege API keys when possible

## Next Steps

1. ✅ **Start with OpenAI** - It's fully implemented and ready to use
2. 📝 **Complete other providers** - Uncomment TODO comments as needed
3. 📚 **Read detailed docs** - See `comfy_api_nodes/CUSTOM_API_README.md`
4. 🧪 **Test thoroughly** - Start with simple workflows
5. 🔒 **Secure your keys** - Follow security best practices

## Need Help?

- **Detailed documentation**: `comfy_api_nodes/CUSTOM_API_README.md`
- **Example config**: `comfy_api_nodes/custom_api_config.json.example`
- **Provider API docs**: Check your provider's official documentation

## What's Next?

This implementation provides a foundation for custom API usage. You can:

1. Complete the remaining providers by uncommenting TODO code
2. Add support for additional authentication methods
3. Implement request logging and monitoring
4. Add retry logic specific to each provider
5. Create provider-specific configuration options

## Summary

✅ **What Works Now:**
- Configuration system (JSON + environment variables)
- OpenAI nodes fully functional with custom APIs
- All other nodes prepared with TODO comments
- Automatic path transformation
- Secure API key handling
- Backward compatible with ComfyUI API

⚠️ **What Needs Attention:**
- Uncomment configuration code in other provider node files
- Test with each provider you intend to use
- Add your API keys to configuration

📁 **Important Files:**
- Your config: `comfy_api_nodes/custom_api_config.json`
- Documentation: `comfy_api_nodes/CUSTOM_API_README.md`
- This guide: `CUSTOM_API_SETUP_GUIDE.md`
