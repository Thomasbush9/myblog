import re

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content with proper nested structure support"""
    frontmatter = {}
    body = content
    
    match = re.match(r'^---\s*\n(.*??)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return frontmatter, body
    
    yaml_text = match.group(1)
    body = match.group(2)
    
    lines = yaml_text.split('\n')
    stack = [(0, frontmatter)]  # Stack of (indent_level, current_dict)
    current_list = None
    list_stack = []  # Stack to track nested lists
    
    def get_indent(line):
        return len(line) - len(line.lstrip())
    
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        
        # Skip empty lines
        if not line.strip():
            continue
        
        indent = get_indent(line)
        stripped = line.strip()
        
        # Pop from stack until we find the right indentation level
        while stack and indent < stack[-1][0]:
            if current_list and list_stack and list_stack[-1][0] >= stack[-1][0]:
                current_list = list_stack[-1][1] if len(list_stack) > 1 else None
                list_stack.pop()
            stack.pop()
        
        # Handle array items
        if stripped.startswith('- '):
            item = stripped[2:].strip()
            
            if current_list is not None:
                # We're inside a list
                if ':' in item:
                    # Object in array
                    k, v = item.split(':', 1)
                    k = k.strip()
                    v = v.strip(" '\""")
                    
                    if not v:
                        # Nested object in array
                        check_indent = indent + 2
                        check_i = i
                        
                        # Find all lines that belong to this object
                        props = {}
                        while check_i < len(lines):
                            next_line = lines[check_i]
                            next_indent = get_indent(next_line)
                            
                            if next_indent < check_indent:
                                break
                            
                            if next_indent == check_indent:
                                next_stripped = next_line.strip()
                                if ':' in next_stripped:
                                    nk, nv = next_stripped.split(':', 1)
                                    props[nk.strip()] = nv.strip(" '\"""")
                                else:
                                    break
                                check_i += 1
                            else:
                                break
                        
                        current_list.append(props)
                        i = check_i
                    else:
                        current_list.append({k: v})
                        i += 1
                else:
                    # Simple value
                    current_list.append(item.strip(" '\"""))
                    i += 1
            else:
                # Standalone array items - this shouldn't happen in valid frontmatter
                i += 1
            
            continue
        
        # Regular key-value pairs
        if ':' in stripped:
            key, value = stripped.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            current_dict = stack[-1][1]
            
            if value.startswith('[') and value.endswith(']'):
                # Inline array
                items = [v.strip().strip(" '\""") for v in value[1:-1].split(',') if v.strip()]
                current_dict[key] = items
                current_list = items
                list_stack.append((indent, current_list))
            elif value:
                # Simple value
                current_dict[key] = value.strip(" '\"""")
                current_list = None
            else:
                # Empty value - might be followed by nested structure or array
                # Check next line to determine
                if i < len(lines):
                    next_indent = get_indent(lines[i])
                    
                    if lines[i].strip().startswith('- '):
                        # Array
                        current_dict[key] = []
                        current_list = current_dict[key]
                        list_stack.append((indent, current_list))
                    elif next_indent > indent:
                        # Nested object
                        nested = {}
                        current_dict[key] = nested
                        stack.append((next_indent, nested))
                        current_list = None
                    else:
                        # Empty string
                        current_dict[key] = ''
                        current_list = None
                else:
                    # Empty string at end
                    current_dict[key] = ''
                    current_list = None
    
    return frontmatter, body


print("=" * 70)
print("TESTING FIXED PARSER")
print("=" * 70)

# Test with the problematic structure
test_content = """---
title: "About Me"
about:
  template: jolla
  links:
    - icon: twitter
      text: Twitter
      href: https://x.com/thomasbush99
    - icon: github
      text: Github
      href: https://github.com/Thomasbush9
---

Content here
"""

fm, body = parse_frontmatter(test_content)

import pprint
print("\\nFrontmatter structure:")
pprint.pprint(fm)

print("\\nAbout section:")
pprint.pprint(fm.get('about'))

print("\\nLinks from about:")
pprint.pprint(fm.get('about', {}).get('links'))

print("\\n" + "=" * 70)
print("Now testing with the REAL about.qmd file:")
print("=" * 70)

# Test with real about.qmd
with open('/Users/thomasbush/Documents/myblog/about.qmd', 'r') as f:
    real_content = f.read()

fm2, body2 = parse_frontmatter(real_content)
print("\\nAbout section:")
pprint.pprint(fm2.get('about'))

correct_structure = isinstance(fm2.get('about'), dict) and 'links' in fm2.get('about', {})
print("\\nCorrect structure:", correct_structure)
print("Links found:", len(fm2.get('about', {}).get('links', [])))
