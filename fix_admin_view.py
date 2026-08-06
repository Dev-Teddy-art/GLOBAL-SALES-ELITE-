import re

with open('src/components/ReferralTree.tsx', 'r') as f:
    content = f.read()

content = content.replace("{focusedUserId && (", "{focusedUserId && isAdminView && (")

with open('src/components/ReferralTree.tsx', 'w') as f:
    f.write(content)
