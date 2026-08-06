import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

content = content.replace("BadgeDollar", "Banknote")

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
