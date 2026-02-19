#!/usr/bin/env python3
import re

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
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1]
        return s
    
    stack = [(0, frontmatter, None)]
    i = 0
    
    while i < len(lines):
        line = lines[i]
        i += 1
        
        if not line or line.strip().startswith('#'):
            continue
        
        indent = get_indent(line)
        stripped = line.strip()
        
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        
        current_dict = stack[-1][1]
        
        if ':' not in stripped and not stripped.startswith('- '):
            continue
        
        if stripped.startswith('- '):
            item_content = stripped[2:].strip()
            parent_key = stack[-1][2]
            
            if parent_key and isinstance(current_dict.get(parent_key), list):
                target_list = current_dict[parent_key]
                
                if ':' in item_content:
                    k, v = item_content.split(':', 1)
                    k = k.strip()
                    v = strip_quotes(v.strip())
                    
                    if not v:
                        obj = {}
                        check_i = i
                        check_indent = indent + 2
                        
                        while check_i < len(lines):
                            sub_line = lines[check_i]
                            sub_indent = get_indent(sub_line)
                            
                            if sub_indent < check_indent:
                                break
                            
                            if sub_indent == check_indent and ':' in sub_line:
                                sk, sv = sub_line.split(':', 1)
                                obj[sk.strip()] = strip_quotes(sv.strip())
                                i = check_i + 1
                            else:
                                break
                            
                            check_i += 1
                        
                        target_list.append(obj)
                    else:
                        target_list.append({k: v})
                        i += 1
                else:
                    target_list.append(strip_quotes(item_content))
                    i += 1
            
            continue
        
        if ':' in stripped:
            key, value = stripped.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if value.startswith('[') and value.endswith(']'):
                items = []
                for item in value[1:-1].split(','):
                    item = item.strip()
                    if item:
                        items.append(strip_quotes(item))
                current_dict[key] = items
            elif value:
                current_dict[key] = strip_quotes(value)
            else:
                if i < len(lines):
                    next_line = lines[i]
                    next_indent = get_indent(next_line)
                    
                    if next_line.strip().startswith('- '):
                        current_dict[key] = []
                        stack.append((next_indent, current_dict[key], key))
                    elif next_indent > indent:
                        nested = {}
                        current_dict[key] = nested
                        stack.append((next_indent, nested, key))
                    else:
                        current_dict[key] = ''
                else:
                    current_dict[key] = ''
    
    return frontmatter, body

# Comparison with current parser
print("PARSER FIX COMPARISON")
print("=" * 80)
print()

with open('about.qmd', 'r') as f:
    content = f.read()

# Test current parser
import sys
sys.path.insert(0, '/Users/thomasbush/Documents/myblog')
from build_simple import parse_frontmatter as current_parse

current_fm, _ = current_parse(content)

print("CURRENT PARSER OUTPUT:")
print("  - 'about' type:", type(current_fm.get('about')).__name__)
print("  - 'about' value:", repr(current_fm.get('about')))
print("  - Is 'links' nested in about?", 'links' in current_fm.get('about', {}))
print("  - Top-level 'links' value:", repr(current_fm.get('links')))
print()

# Test fixed parser
fixed_fm, _ = parse_frontmatter_fixed(content)

print("FIXED PARSER OUTPUT:")
print("  - 'about' type:", type(fixed_fm.get('about')).__name__)
print("  - Is 'about' a dict?", isinstance(fixed_fm.get('about'), dict))
if isinstance(fixed_fm.get('about'), dict):
    print("  - 'template' value:", repr(fixed_fm['about'].get('template')))
    print("  - Is 'links' in about?", 'links' in fixed_fm['about'])
    if 'links' in fixed_fm['about']:
        print("  - Number of links:", len(fixed_fm['about']['links']))
        for link in fixed_fm['about']['links'][:3]:
            print(f"    * {link.get('icon')}: {link.get('text')}")
print()

success = isinstance(fixed_fm.get('about'), dict) and 'links' in fixed_fm.get('about', {})
print("SUCCESS!" if success else "FAILED")

# Show the full structure if successful
if success:
    print()
    print("FULL STRUCTURE (about section):")
    import json
    print(json.dumps(fixed_fm['about'], indent=2))
