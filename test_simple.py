import re, json

def parse_frontmatter_fixed(content):
    frontmatter = {}
    body = content
    
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return frontmatter, body
    
    yaml_text = match.group(1)
    body = match.group(2)
    
    lines = [line.rstrip() for line in yaml_text.split("\n")]
    
    def get_indent(line):
        return len(line) - len(line.lstrip())
    
    def strip_quotes(s):
        return s.strip(" \'"")
    
    stack = [(0, frontmatter, None)]
    i = 0
    
    while i < len(lines):
        line = lines[i]
        i += 1
        
        if not line or line.strip().startswith("#"):
            continue
        
        indent = get_indent(line)
        stripped = line.strip()
        
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        
        current_dict = stack[-1][1]
        
        if ":" not in stripped and not stripped.startswith("- "):
            continue
        
        if stripped.startswith("- "):
            item_content = stripped[2:].strip()
            parent_key = stack[-1][2]
            
            if parent_key and isinstance(current_dict.get(parent_key), list):
                target_list = current_dict[parent_key]
                
                if ":" in item_content:
                    k, v = item_content.split(":", 1)
                    k = k.strip()
                    v = strip_quotes(v.strip())
                    
                    if v == "":
                        obj = {}
                        check_i = i
                        check_indent = indent + 2
                        
                        while check_i < len(lines):
                            sub_line = lines[check_i]
                            sub_indent = get_indent(sub_line)
                            
                            if sub_indent < check_indent:
                                break
                            
                            if sub_indent == check_indent and ":" in sub_line:
                                sk, sv = sub_line.split(":", 1)
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
        
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            
            if value.startswith("[") and value.endswith("]"):
                items = [strip_quotes(v.strip()) for v in value[1:-1].split(",") if v.strip()]
                current_dict[key] = items
            elif value:
                current_dict[key] = strip_quotes(value)
            else:
                if i < len(lines):
                    next_line = lines[i]
                    next_indent = get_indent(next_line)
                    
                    if next_line.strip().startswith("- "):
                        current_dict[key] = []
                        stack.append((next_indent, current_dict[key], key))
                    elif next_indent > indent:
                        nested = {}
                        current_dict[key] = nested
                        stack.append((next_indent, nested, key))
                    else:
                        current_dict[key] = ""
                else:
                    current_dict[key] = ""
    
    return frontmatter, body


print("TEST WITH REAL about.qmd:")
print("=" * 70)

with open("about.qmd", "r") as f:
    content = f.read()

fm, body = parse_frontmatter_fixed(content)

print("About section type:", str(type(fm.get("about"))))
print()

if isinstance(fm.get("about"), dict):
    print("About section (JSON format):")
    print(json.dumps(fm.get("about"), indent=2))
else:
    print("About section:", fm.get("about"))

print()
links = fm.get("about", {}).get("links", [])
print("Links found:", len(links))
for link in links:
    icon = link.get('icon', '?')
    text = link.get('text', '?')
    href = link.get('href', '#')
    print(f"  - {icon}: {text} -> {href}")
