import re

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content with proper nested structure support"""
    frontmatter = {}
    body = content
    
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return frontmatter, body
    
    yaml_text = match.group(1)
    body = match.group(2)
    
    lines = yaml_text.split('\n')
    stack = [(0, frontmatter)]
    current_list = None
    list_stack = []
    
    def get_indent(line):
        return len(line) - len(line.lstrip())
    
    def strip_quotes(s):
        return s.strip(" '\""")
    
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        
        if not line.strip():
            continue
        
        indent = get_indent(line)
        stripped = line.strip()
        
        while stack and indent < stack[-1][0]:
            if current_list and list_stack and list_stack[-1][0] >= stack[-1][0]:
                current_list = list_stack[-1][1] if len(list_stack) > 1 else None
                list_stack.pop()
            stack.pop()
        
        if stripped.startswith('- '):
            item = stripped[2:].strip()
            
            if current_list is not None:
                if ':' in item:
                    k, v = item.split(':', 1)
                    k = k.strip()
                    v = strip_quotes(v)
                    
                    if not v:
                        check_indent = indent + 2
                        check_i = i
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
                                    props[nk.strip()] = strip_quotes(nv)
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
                    current_list.append(strip_quotes(item))
                    i += 1
            else:
                i += 1
            
            continue
        
        if ':' in stripped:
            key, value = stripped.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            current_dict = stack[-1][1]
            
            if value.startswith('[') and value.endswith(']'):
                items = [strip_quotes(v) for v in value[1:-1].split(',') if v.strip()]
                current_dict[key] = items
                current_list = items
                list_stack.append((indent, current_list))
            elif value:
                current_dict[key] = strip_quotes(value)
                current_list = None
            else:
                if i < len(lines):
                    next_indent = get_indent(lines[i])
                    
                    if lines[i].strip().startswith('- '):
                        current_dict[key] = []
                        current_list = current_dict[key]
                        list_stack.append((indent, current_list))
                    elif next_indent > indent:
                        nested = {}
                        current_dict[key] = nested
                        stack.append((next_indent, nested))
                        current_list = None
                    else:
                        current_dict[key] = ''
                        current_list = None
                else:
                    current_dict[key] = ''
                    current_list = None
    
    return frontmatter, body

print("=" * 70)
print("TESTING FIXED PARSER WITH REAL FILE")
print("=" * 70)

with open("about.qmd", "r") as f:
    real_content = f.read()

fm2, body2 = parse_frontmatter(real_content)

import pprint
print("\nAbout section:")
pprint.pprint(fm2.get("about"))

correct = isinstance(fm2.get("about"), dict) and "links" in fm2.get("about", {})
print("\nCorrect structure:", correct)
print("Number of links:", len(fm2.get("about", {}).get("links", [])))

if correct:
    print("\nLinks details:")
    for link in fm2["about"]["links"]:
        print(f"  - {link.get('icon')}: {link.get('text')} -> {link.get('href')}")
