#!/bin/bash
# Apply custom API configuration support to all API node files

echo "================================================"
echo "Applying Custom API Support to All API Nodes"
echo "================================================"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Array of node files and their providers
declare -A nodes=(
    ["nodes_bfl.py"]="bfl"
    ["nodes_bytedance.py"]="bytedance"
    ["nodes_gemini.py"]="gemini"
    ["nodes_ideogram.py"]="ideogram"
    ["nodes_kling.py"]="kling"
    ["nodes_ltxv.py"]="ltxv"
    ["nodes_luma.py"]="luma"
    ["nodes_minimax.py"]="minimax"
    ["nodes_moonvalley.py"]="moonvalley"
    ["nodes_pika.py"]="pika"
    ["nodes_pixverse.py"]="pixverse"
    ["nodes_recraft.py"]="recraft"
    ["nodes_rodin.py"]="rodin"
    ["nodes_runway.py"]="runway"
    ["nodes_sora.py"]="sora"
    ["nodes_tripo.py"]="tripo"
    ["nodes_veo2.py"]="veo2"
    ["nodes_vidu.py"]="vidu"
    ["nodes_wan.py"]="wan"
)

# Counter for statistics
total=0
success=0
skipped=0

# Process each node file
for node_file in "${!nodes[@]}"; do
    provider="${nodes[$node_file]}"
    total=$((total + 1))
    
    if [ ! -f "$node_file" ]; then
        echo "⚠️  Skipping $node_file (not found)"
        skipped=$((skipped + 1))
        continue
    fi
    
    # Skip if already fully modified (check for actual implementation, not just comments)
    if grep -q "custom_api_base, custom_auth_kwargs = apply_custom_config" "$node_file"; then
        echo "✓ $node_file already has custom API support"
        success=$((success + 1))
        continue
    fi
    
    echo "Processing $node_file ($provider)..."
    python3 apply_custom_api_to_node.py "$node_file" "$provider" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "  ✓ Successfully processed"
        success=$((success + 1))
    else
        echo "  ✗ Failed to process"
    fi
    echo ""
done

echo "================================================"
echo "Summary:"
echo "  Total files: $total"
echo "  Successfully processed: $success"
echo "  Skipped: $skipped"
echo "================================================"
echo ""
echo "⚠️  IMPORTANT: The files have been updated with TODO comments."
echo "   You need to manually uncomment and verify the configuration"
echo "   code in each file before the custom API will work."
echo ""
echo "   See CUSTOM_API_README.md for detailed instructions."
echo ""
echo "   Modified files are in: $(pwd)"
echo "   Backup files are in: $(pwd)/../custom_api_nodes/"
