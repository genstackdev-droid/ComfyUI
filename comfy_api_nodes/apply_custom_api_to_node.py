#!/usr/bin/env python3
"""
Helper script to apply custom API configuration support to additional API node files.

Usage:
    python apply_custom_api_to_node.py nodes_stability.py stability
    python apply_custom_api_to_node.py nodes_runway.py runway

This will:
1. Add necessary imports
2. Add comments showing where to insert custom API configuration
3. Create a backup in custom_api_nodes/
"""

import sys
import shutil
from pathlib import Path

def show_usage():
    print("Usage: python apply_custom_api_to_node.py <node_file> <provider_name>")
    print("\nExamples:")
    print("  python apply_custom_api_to_node.py nodes_stability.py stability")
    print("  python apply_custom_api_to_node.py nodes_runway.py runway")
    print("  python apply_custom_api_to_node.py nodes_luma.py luma")
    sys.exit(1)

def add_import_if_needed(content: str) -> tuple[str, bool]:
    """Add custom API import if not present."""
    import_line = "from comfy_api_nodes.custom_api_helpers import apply_custom_config, transform_path_for_custom_api"
    
    if "custom_api_helpers" in content:
        return content, False
    
    lines = content.split('\n')
    last_import_idx = -1
    
    # Find last comfy_api_nodes import
    for i, line in enumerate(lines):
        if 'from comfy_api_nodes' in line or 'import comfy_api_nodes' in line:
            last_import_idx = i
    
    if last_import_idx >= 0:
        lines.insert(last_import_idx + 1, import_line)
        return '\n'.join(lines), True
    
    return content, False

def add_config_comments(content: str, provider: str) -> tuple[str, int]:
    """Add helpful comments before operation calls."""
    lines = content.split('\n')
    modifications = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Look for operation creation
        if 'operation = SynchronousOperation(' in line or 'operation = PollingOperation(' in line:
            indent = len(line) - len(line.lstrip())
            indent_str = ' ' * indent
            
            # Check if we already added comments
            if i > 0 and 'Apply custom API configuration' in lines[i-1]:
                i += 1
                continue
            
            # Add comment block
            comment_block = [
                f"{indent_str}# TODO: Apply custom API configuration",
                f"{indent_str}# Uncomment and modify the following lines:",
                f"{indent_str}# custom_api_base, custom_auth_kwargs = apply_custom_config(",
                f"{indent_str}#     provider=\"{provider}\",",
                f"{indent_str}#     auth_kwargs=kwargs,",
                f"{indent_str}#     path=path  # Make sure 'path' variable exists",
                f"{indent_str}# )",
                f"{indent_str}# custom_path = transform_path_for_custom_api(path, provider=\"{provider}\")",
                f"{indent_str}#",
                f"{indent_str}# Then modify the operation to use:",
                f"{indent_str}#   - path=custom_path instead of path=path",
                f"{indent_str}#   - api_base=custom_api_base",
                f"{indent_str}#   - auth_kwargs=custom_auth_kwargs instead of auth_kwargs=kwargs",
                f"{indent_str}",
            ]
            
            # Insert comment block before operation
            for j, comment_line in enumerate(comment_block):
                lines.insert(i + j, comment_line)
            
            modifications += 1
            i += len(comment_block) + 1
        else:
            i += 1
    
    return '\n'.join(lines), modifications

def main():
    if len(sys.argv) != 3:
        show_usage()
    
    node_file = sys.argv[1]
    provider = sys.argv[2].lower()
    
    script_dir = Path(__file__).parent
    source_path = script_dir / node_file
    custom_path = script_dir.parent / "custom_api_nodes" / node_file
    
    if not source_path.exists():
        print(f"Error: File {source_path} not found!")
        sys.exit(1)
    
    print(f"Processing {node_file} for provider '{provider}'...")
    print()
    
    # Read the file
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add import
    content, import_added = add_import_if_needed(content)
    if import_added:
        print("✓ Added custom API helpers import")
    else:
        print("- Import already present")
    
    # Add configuration comments
    content, mod_count = add_config_comments(content, provider)
    if mod_count > 0:
        print(f"✓ Added configuration comments to {mod_count} operation(s)")
    else:
        print("- No operations found or already commented")
    
    # Save back to original location
    with open(source_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated {source_path}")
    
    # Copy to custom_api_nodes
    custom_path.parent.mkdir(exist_ok=True)
    shutil.copy2(source_path, custom_path)
    print(f"✓ Backup created at {custom_path}")
    
    print()
    print("Done! Next steps:")
    print(f"1. Open {source_path}")
    print("2. Find the TODO comments")
    print("3. Uncomment and verify the configuration code")
    print("4. Test with your custom API configuration")
    print()
    print("See CUSTOM_API_README.md for detailed instructions.")

if __name__ == "__main__":
    main()
