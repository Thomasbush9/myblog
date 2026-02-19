#!/bin/bash
# Image optimization script for macOS using sips
# Resizes large images to web-friendly sizes

echo "🖼️  Blog Image Optimizer (macOS)"
echo "=================================="

SITE_DIR="_site"

if [ ! -d "$SITE_DIR" ]; then
    echo "✗ _site directory not found. Run build_simple.py first."
    exit 1
fi

echo "🔍 Optimizing images for web..."

OPTIMIZED_COUNT=0
TOTAL_SAVED=0

# Function to optimize image
optimize_image() {
    local img_path="$1"
    local max_width="$2"
    local description="$3"
    
    local original_size=$(stat -f%z "$img_path" 2>/dev/null || stat -c%s "$img_path" 2>/dev/null)
    
    # Get current width
    local width=$(sips -g pixelWidth "$img_path" | grep pixelWidth | awk '{print $2}')
    
    if [ "$width" -gt "$max_width" ]; then
        echo "  🔧 $description (resizing from ${width}px)"
        sips -Z "$max_width" "$img_path" >/dev/null 2>&1
        
        local new_size=$(stat -f%z "$img_path" 2>/dev/null || stat -c%s "$img_path" 2>/dev/null)
        local saved=$((original_size - new_size))
        TOTAL_SAVED=$((TOTAL_SAVED + saved))
        
        if [ $saved -gt 0 ]; then
            local saved_kb=$((saved / 1024))
            echo "      saved ${saved_kb}KB"
        fi
        
        OPTIMIZED_COUNT=$((OPTIMIZED_COUNT + 1))
    else
        local size_kb=$((original_size / 1024))
        echo "  ✓ $description: ${size_kb}KB (no change)"
    fi
}

# Find all image directories
for img_dir in $(find "$SITE_DIR" -name "*_images" -type d); do
    echo ""
    echo "📁 Processing $(basename "$img_dir")/"
    
    # Optimize all images in this directory
    find "$img_dir" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | while read img_path; do
        filename=$(basename "$img_path")
        optimize_image "$img_path" 1200 "$filename"
    done
done

# Optimize profile image
PROFILE="$SITE_DIR/profile.jpg"
if [ -f "$PROFILE" ]; then
    echo ""
    optimize_image "$PROFILE" 400 "profile.jpg"
fi

# Summary
echo ""
echo "=================================="
if [ $OPTIMIZED_COUNT -gt 0 ]; then
    total_saved_mb=$((TOTAL_SAVED / 1024 / 1024))
    echo "✅ Optimized $OPTIMIZED_COUNT images"
    echo "💾 Saved ${total_saved_mb}MB total"
else
    echo "✓ No images needed optimization"
fi

echo ""
echo "✨ Image optimization complete!"
echo ""
echo "Next steps:"
echo "  cd _site && python3 -m http.server 8000"
