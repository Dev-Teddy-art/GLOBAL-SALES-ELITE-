import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = re.sub(r'text-gray-600 dark:text-gray-[0-9]+ dark:text-white/[0-9]+', 'text-gray-600 dark:text-gray-400', content)
content = re.sub(r'text-gray-900 dark:text-gray-600 dark:text-white/[0-9]+', 'text-gray-900 dark:text-gray-300', content)
content = re.sub(r'text-gray-600 dark:text-gray-[0-9]+ dark:text-gray-[0-9]+ dark:text-gray-[0-9]+ dark:text-white/[0-9]+', 'text-gray-500 dark:text-gray-400', content)

with open('src/App.tsx', 'w') as f:
    f.write(content)

