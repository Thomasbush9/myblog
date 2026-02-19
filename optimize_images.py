#!/usr/bin/env python3
"""
Image optimization script for the blog
- Resizes large images to web-friendly sizes
- Keeps aspect ratio
- Overwrites images in _site directory
"""

import os
import sys
from pathlib import Path

# Try to import Pillow, fallback to warning if not available
try:
    from PIL import Image

    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("WARNING: Pillow not installed. Install with: pip install Pillow")
    print(
        "Will skip image optimization. Site will still work but images will be larger."
    )


def optimize_image(image_path, max_width=1200, quality=85):
    """Optimize a single image"""
    if not HAS_PILLOW:
        return False

    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")

            # Get current dimensions
            width, height = img.size

            # Skip if already small enough
            if width <= max_width:
                return False

            # Calculate new dimensions maintaining aspect ratio
            ratio = max_width / width
            new_width = max_width
            new_height = int(height * ratio)

            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save optimized image
            if image_path.suffix.lower() == ".png":
                img.save(image_path, optimize=True)
            else:
                img.save(image_path, quality=quality, optimize=True)

            return True
    except Exception as e:
        print(f"  Error processing {image_path.name}: {e}")
        return False


def optimize_all_images():
    """Optimize all images in _site directory"""
    if not HAS_PILLOW:
        print("\n✗ Image optimization skipped (Pillow not available)")
        return False

    site_dir = Path("_site")
    if not site_dir.exists():
        print("✗ _site directory not found. Run build_simple.py first.")
        return False

    print("🔍 Optimizing images for web...")

    optimized_count = 0
    total_saved = 0

    # Find all image directories
    for img_dir in site_dir.rglob("*_images"):
        if not img_dir.is_dir():
            continue

        print(f"\n📁 Processing {img_dir.relative_to(site_dir)}/")

        for img_path in img_dir.iterdir():
            if img_path.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
                continue

            original_size = img_path.stat().st_size

            if optimize_image(img_path):
                new_size = img_path.stat().st_size
                saved = original_size - new_size
                total_saved += saved
                optimized_count += 1

                saved_kb = saved / 1024
                print(f"  🔧 {img_path.name}: saved {saved_kb:.1f}KB")
            else:
                size_kb = original_size / 1024
                print(f"  ✓ {img_path.name}: {size_kb:.0f}KB (no change)")

    # Optimize profile image
    profile = site_dir / "profile.jpg"
    if profile.exists():
        original_size = profile.stat().st_size
        if optimize_image(profile, max_width=400):
            new_size = profile.stat().st_size
            saved = original_size - new_size
            total_saved += saved
            optimized_count += 1

            saved_kb = saved / 1024
            print(f"  🔧 profile.jpg: saved {saved_kb:.1f}KB")
        else:
            size_kb = original_size / 1024
            print(f"  ✓ profile.jpg: {size_kb:.0f}KB (no change)")

    if optimized_count > 0:
        total_saved_mb = total_saved / 1024 / 1024
        print(f"\n✅ Optimized {optimized_count} images")
        print(f"💾 Saved {total_saved_mb:.2f} MB total")
    else:
        print("\n✓ No images needed optimization")

    return True


if __name__ == "__main__":
    print("🖼️ Blog Image Optimizer")
    print("=" * 50)

    if not HAS_PILLOW:
        print("\n⚠️  Pillow not installed. Install with:")
        print("   pip install Pillow\n")
        print("Continuing without optimization...")
        sys.exit(0)

    optimize_all_images()

    print("\n" + "=" * 50)
    print("✨ Image optimization complete!")
    print("\nNext steps:")
    print("  cd _site && python3 -m http.server 8000")
