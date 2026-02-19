#!/bin/bash
# Quick local preview

echo "🌐 Starting local preview..."
echo "Opening http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

cd _site && python3 -m http.server 8000
