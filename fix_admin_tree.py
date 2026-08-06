import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

content = content.replace('text-lg text-gray-900 dark:text-white shadow-inner', 'text-lg text-white shadow-inner')

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
