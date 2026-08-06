import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_ref = "  const refCode = searchParams.get('ref') || '';"
new_ref = """  const rawRef = searchParams.get('ref') || '';
  const refCode = rawRef.includes('-') ? rawRef.split('-').pop() : rawRef;"""
content = content.replace(old_ref, new_ref)

with open('src/App.tsx', 'w') as f:
    f.write(content)
