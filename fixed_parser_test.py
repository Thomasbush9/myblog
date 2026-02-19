import re
import json

def parse_frontmatter_fixed(content):
    """Fixed YAML frontmatter parser with nested structure support"""
    frontmatter = {}
    body = content
    
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return frontmatter, body
    
    yaml_text = match.group(1)
    body = match.group(2)
    lines = [line.rstrip() for line in yaml_text.split('\n')]
    
    def get_indent(line):
        return len(line) - len(line.lstrip())
    
    def strip_quotes(s):
        s = s.strip()
        if s and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            return s[1:-1]
        return s
    
    # Stack tracks: (indent_level, current_dict, parent_key)
    stack = [(0, frontmatter, None)]
    i = 0
    
    while i < len(lines):
        line = lines[i]
        i += 1
        
        if not line or line.strip().startswith('#'):
            continue
        
        indent = get_indent(line)
        stripped = line.strip()
        
        # Pop stack to find correct context
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        
        current_dict = stack[-1][1]
        parent_key = stack[-1][2]
        
        # Skip if no key-value pair or array item
        if ':' not in stripped and not stripped.startswith('- '):
            continue
        
        # Handle array items
        if stripped.startswith('- '):
            if not parent_key or not isinstance(current_dict.get(parent_key), list):
                continue
                
            item_text = stripped[2:].strip()
            obj = {}
            
            # Parse first property
            if ':' in item_text:
                k, v = item_text.split(':', 1)
                obj[k.strip()] = strip_quotes(v.strip())
            else:
                obj = strip_quotes(item_text)
            
            # Parse additional indented properties
            while i < len(lines) and get_indent(lines[i]) > indent:
                sub_line = lines[i].strip()
                if ':' in sub_line:
                    sk, sv = sub_line.split(':', 1)
                    if isinstance(obj, dict):
                        obj[sk.strip()] = strip_quotes(sv.strip())
                i += 1
            
            current_dict[parent_key].append(obj)
            continue
        
        # Handle key-value pairs
        key, value = stripped.split(':', 1)
        key = key.strip()
        value = value.strip()
        
        if value.startswith('[') and value.endswith(']'):
            # Inline array
            items = []
            for item in value[1:-1].split(','):
                item = item.strip()
                if item:
                    items.append(strip_quotes(item))
            current_dict[key] = items
        elif value:
            # Simple value
            current_dict[key] = strip_quotes(value)
        else:
            # Empty value - check if nested structure follows
            if i >= len(lines):
                current_dict[key] = ''
                continue
            
            next_indent = get_indent(lines[i])
            next_stripped = lines[i].strip()
            
            if next_stripped.startswith('- '):
                # Array follows
                current_dict[key] = []
                stack.append((next_indent, current_dict[key], key))
                # Don't advance i - process the array item in next iteration
                i -= 1
            elif next_indent > indent:
                # Nested object follows
                nested = {}
                current_dict[key] = nested
                stack.append((next_indent, nested, key))
                # Don't advance i - process the nested content in next iteration
                i -= 1
            else:
                # Empty string
                current_dict[key] = ''
    
    return frontmatter, body

# Test with real about.qmd
with open('/Users/thomasbush/Documents/myblog/about.qmd', 'r') as f:
    content = f.read()

fm, body = parse_frontmatter_fixed(content)

print("RESULT:")
print("=" * 70)
print("About type:", type(fm.get('about')).__name__)
print()

if isinstance(fm.get('about'), dict):
    print("About section:")
    print(json.dumps(fm.get('about'), indent=2))
    print()
    print("Links count:", len(fm.get('about', {}).get('links', [])))
else:
    print("About value:", repr(fm.get('about')))
    print("Links at root:", 'links' in fm)
    print("Template at root:", 'template' in fm)
