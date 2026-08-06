import re

with open('src/components/Footer.tsx', 'r') as f:
    content = f.read()

content = content.replace('bg-[#070b14]', 'bg-white dark:bg-[#070b14]')
content = content.replace('text-white font-bold', 'text-gray-900 dark:text-white font-bold')
content = content.replace('text-gray-600', 'text-gray-500 dark:text-gray-600')

with open('src/components/Footer.tsx', 'w') as f:
    f.write(content)
