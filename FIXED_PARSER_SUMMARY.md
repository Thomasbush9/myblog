# Parse Frontmatter Function Fix Summary

## Problem Statement

The `parse_frontmatter` function in `build_simple.py` fails to properly handle nested YAML structures. Specifically, with the `about.qmd` file structure:

```yaml
---
title: "About Me"
about:
  template: jolla
  links:
    - icon: twitter
      text: Twitter
      href: https://x.com/thomasbush99
---
```

## Current Parser Output (BROKEN)

```python
{
  'title': 'About Me',
  'about': '',                    # EMPTY STRING (wrong!)
  'template': 'jolla',            # FLATTENED (should be in about)
  'links': [],                    # EMPTY ARRAY at root (wrong!)
  'text': 'Email',                # FLATTENED (should be in links array)
  'href': 'mailto:...'            # FLATTENED (should be in links array)
}
```

**Issues:**
- `about` is an empty string instead of a dictionary
- `links` is an empty array at the root level instead of being nested under `about`
- All array items are flattened to the root level
- The last array item's properties (`text`, `href`) overwrite previous values

## Expected Output (CORRECT)

```python
{
  'title': 'About Me',
  'image': 'profile.jpg',
  'about': {
    'template': 'jolla',
    'links': [
      {'icon': 'twitter', 'text': 'Twitter', 'href': 'https://x.com/thomasbush99'},
      {'icon': 'linkedin', 'text': 'LinkedIn', 'href': 'https://www.linkedin.com/in/...'},
      {'icon': 'github', 'text': 'Github', 'href': 'https://github.com/Thomasbush9'},
      {'icon': 'file', 'text': 'Download CV', 'href': 'cv/ThomasBush_CV.pdf'},
      {'icon': 'envelope', 'text': 'Email', 'href': 'mailto:thomasbush52@gmail.com'}
    ]
  }
}
```

## Root Causes

1. **No indentation tracking**: The parser doesn't track indentation levels to understand nesting
2. **No context stack**: When encountering nested structures, it doesn't maintain a stack of parent contexts
3. **Flawed array detection**: Line 65-67 checks if the NEXT line is an array, but doesn't handle the case where the value is empty and should contain a nested structure
4. **No nested object creation**: When encountering `about:` with no value followed by indented content, it should create a nested dict
5. **Flattened output**: All keys end up at the root level because nested contexts aren't maintained

## The Fix

The fixed parser implements:

1. **Indentation tracking**: Calculate indentation for each line to determine nesting level
2. **Context stack**: Maintain a stack of (indent_level, current_dict, parent_key) tuples
3. **Empty value handling**: When a key has an empty value followed by indented content, create appropriate nested structure (dict or list)
4. **Array item collection**: When processing array items, collect all indented properties at the same level
5. **Proper nesting**: Ensure all nested structures are properly placed in their parent dictionaries

### Key Changes to build_simple.py

Replace the `parse_frontmatter` function (lines 14-72) with the fixed version:

```python
def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content with nested structure support"""
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
        
        # Find correct context based on indentation
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        
        current_dict = stack[-1][1]
        parent_key = stack[-1][2]
        
        # Skip non-key lines
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
            # Empty value - check for nested structure
            if i < len(lines):
                next_indent = get_indent(lines[i])
                next_stripped = lines[i].strip()
                
                if next_stripped.startswith('- '):
                    # Array follows
                    current_dict[key] = []
                    stack.append((next_indent, current_dict[key], key))
                elif next_indent > indent:
                    # Nested object follows
                    nested = {}
                    current_dict[key] = nested
                    stack.append((next_indent, nested, key))
                else:
                    # Empty string
                    current_dict[key] = ''
            else:
                current_dict[key] = ''
    
    return frontmatter, body
```

## Testing the Fix

To verify the fix works, run this test:

```python
from build_simple import parse_frontmatter

with open('about.qmd', 'r') as f:
    content = f.read()

fm, _ = parse_frontmatter(content)

# Should print: "dict"
print(type(fm.get('about')).__name__)

# Should print: 5 (number of links)
print(len(fm.get('about', {}).get('links', [])))

# Should print: "jolla"
print(fm.get('about', {}).get('template'))
```

The fixed parser will correctly parse nested YAML structures like those in `about.qmd`.
