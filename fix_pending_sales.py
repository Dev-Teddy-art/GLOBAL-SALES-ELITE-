import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

content = content.replace("pendingSales.length === 0", "sales.length === 0")

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
