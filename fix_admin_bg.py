import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    'bg-[#1E3A8A] opacity-20',
    'bg-blue-400 dark:bg-blue-900 opacity-5 dark:opacity-20'
)
content = content.replace(
    'bg-[#EF4444] opacity-10',
    'bg-red-400 dark:bg-red-900 opacity-5 dark:opacity-10'
)
content = content.replace(
    'bg-[#1E3A8A]/20',
    'bg-blue-400/5 dark:bg-blue-900/20'
)
content = content.replace(
    'bg-[#EF4444]/10',
    'bg-red-400/5 dark:bg-red-900/10'
)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
