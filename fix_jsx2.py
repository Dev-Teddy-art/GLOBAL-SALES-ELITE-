import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

old_str = """        ) : (
          <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-0">"""
new_str = """        ) : (
          <>
          <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-0">"""
content = content.replace(old_str, new_str)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
