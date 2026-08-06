import re

with open('src/contexts/AuthContext.tsx', 'r') as f:
    content = f.read()

content = content.replace('profileImage?: string;', 'profileImage?: string;\n  avatarUrl?: string;')

with open('src/contexts/AuthContext.tsx', 'w') as f:
    f.write(content)
