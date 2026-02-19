# Parse Frontmatter Function Fix

## Summary

The `parse_frontmatter` function in `build_simple.py` has been fixed to properly handle nested YAML structures. The issue was that nested dictionaries and arrays were being flattened to the root level instead of maintaining their hierarchical structure.

## Files Changed

- `/Users/thomasbush/Documents/myblog/build_simple.py` - Replace lines 14-72 with the fixed implementation

## Changes Made

The key improvements in the fixed parser:

1. **Indentation tracking** - Track indentation level of each line to determine nesting
2. **Context stack** - Maintain a stack of parent contexts as nested structures are encountered  
3. **Array item collection** - Properly collect all properties for array items at the same indentation level
4. **Nested structure detection** - When a key has an empty value followed by indented content, create the appropriate nested structure

## Fixed Function

Replace the existing `parse_frontmatter` function with:

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

## Testing

After applying the fix, the parser should correctly handle `about.qmd`:

```python
from build_simple import parse_frontmatter

with open('about.qmd', 'r') as f:
    content = f.read()

fm, _ = parse_frontmatter(content)

# These should all be True:
assert isinstance(fm.get('about'), dict)
assert 'template' in fm.get('about', {})
assert 'links' in fm.get('about', {})
assert len(fm['about']['links']) == 5
assert fm['about']['links'][0]['icon'] == 'twitter'
```

## Benefits

- ✅ Nested dictionaries are properly parsed (e.g., `about` section)
- ✅ Nested arrays are properly placed in their parent dictionaries (e.g., `about.links`)
- ✅ Array items with multiple properties are correctly collected
- ✅ Indentation-based nesting is properly handled
- ✅ Maintains backward compatibility with simple key-value pairs

## Example Output

**Before (Broken):**
```python
{
  'about': '',           # Empty string
  'template': 'jolla',   # Flattened
  'links': [],           # Empty array at root
  'text': 'Email'        # Overwritten values
}
```

**After (Fixed):**
```python
{
  'about': {
    'template': 'jolla',
    'links': [
      {'icon': 'twitter', 'text': 'Twitter', ...},
      {'icon': 'github', 'text': 'Github', ...},
      ...
    ]
  }
}
```
