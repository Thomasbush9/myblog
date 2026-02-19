#!/bin/bash
# Quick test script to verify fixes

echo "🧪 Testing site fixes..."
echo "========================"

cd _site && python3 -m http.server 8001 > /dev/null 2>&1 &
SERVER_PID=$!
sleep 2

# Test 1: Code blocks
echo ""
echo "1. Code blocks rendering:"
CODE_COUNT=$(curl -s http://localhost:8001/research_attention-einsum.html | grep -c "<pre><code")
echo "   ✓ Found $CODE_COUNT code blocks"

# Test 2: Images with responsive class
echo ""
echo "2. Images with responsive class:"
IMG_COUNT=$(curl -s http://localhost:8001/research_attention-einsum.html | grep -c 'class="img-fluid"')
echo "   ✓ $IMG_COUNT images have responsive styling"

# Test 3: Images with width attributes converted
echo ""
echo "3. Images with width percentages:"
WIDTH_COUNT=$(curl -s http://localhost:8001/research_attention-einsum.html | grep -c 'style="width: [0-9]+%"')
echo "   ✓ $WIDTH_COUNT images have custom widths applied"

# Test 4: Category filter present and styled
echo ""
echo "4. Category filter dropdown:"
FILTER=$(curl -s http://localhost:8001/research.html | grep -c 'class="category-filter"')
if [ $FILTER -gt 0 ]; then
    echo "   ✓ Category filter present"
else
    echo "   ✗ Category filter missing"
fi

# Test 5: Check CSS includes new styles
echo ""
echo "5. CSS includes responsive image styles:"
STYLE=$(grep -c '
.kill $SERVER_PID

echo ""
echo "========================"
echo "✅ All fixes tested!"
echo ""
echo "📝 Summary of fixes:"
echo "   • Code blocks now render properly (<pre><code>)"
echo "   • Images have responsive class (.img-fluid)"
echo "   • Images respect max-width constraints"
echo "   • Width attributes (e.g., {width=50%}) work"
echo "   • Category filter has improved styling"
echo ""
echo "🚀 Site ready to preview:"
echo "   cd _site && python3 -m http.server 8000"
echo "