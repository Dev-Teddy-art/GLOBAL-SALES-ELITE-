import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Fix the container
content = content.replace('bg-white/80 dark:bg-white dark:bg-[#1E293B]/80', 'bg-white/90 dark:bg-[#0B1120] dark:bg-opacity-80')

# Fix the text color of the h3
content = content.replace('h3 className="text-white font-bold', 'h3 className="text-gray-900 dark:text-white font-bold')

with open('src/App.tsx', 'w') as f:
    f.write(content)
