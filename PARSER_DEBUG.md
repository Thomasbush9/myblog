# Parser Debug Report

## Current Parser Issues

### Test Input (about.qmd structure):
```yaml
---
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
```

### Current Parser Output:
```python
{
  'title': 'About Me',
  'about': '',           # Empty string instead of dict
  'template': 'jolla',   # Should be nested under 'about'
  'links': [],           # Empty array at top level
  'text': 'Email',       # Last item from links, at top level!
  'href': 'mailto:...'   # Last item from links, at top level!
}
```

### Expected Output:
```python
{
  'title': 'About Me',
  'about': {             # Dictionary, not string
    'template': 'jolla',
    'links': [           # Array nested under 'about'
      {'icon': 'twitter', 'text': 'Twitter', 'href': '...'},
      {'icon': 'github', 'text': 'Github', 'href': '...'}
    ]
  }
}
```

## Root Causes

1. **No indentation tracking**: The parser doesn't track indentation levels to understand nesting
2. **No context stack**: When encountering nested structures, it doesn't maintain a stack of parent contexts
3. **Array detection is flawed**: Line 65-67 checks if the NEXT line is an array, but doesn't handle the case where the value is empty and should contain a nested structure
4. **Flattened output**: All keys end up at the root level because nested contexts aren't maintained

## The Fix

The fixed parser:
1. Tracks indentation to understand nesting levels
2. Maintains a stack of contexts (dictionaries) as it parses
3. Handles empty values followed by indented content as nested structures
4. Properly nests arrays within their parent dictionaries
