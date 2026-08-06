import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Extract footer block from App.tsx
footer_match = re.search(r'(<footer.*?</footer\s*>)', content, re.DOTALL)
if footer_match:
    footer_jsx = footer_match.group(1)
    # Remove from App.tsx
    content = content.replace(footer_jsx, "")
    
    with open('src/App.tsx', 'w') as f:
        f.write(content)
        
    # Write to Footer.tsx
    footer_component = f"""import React from 'react';
import {{ Logo }} from './Logo';

export function Footer() {{
  return (
{footer_jsx}
  );
}}
"""
    with open('src/components/Footer.tsx', 'w') as f:
        f.write(footer_component)

