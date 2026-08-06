import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

content = content.replace('className="w-full bg-gray-50 flex flex-col font-sans relative pb-12"', 'className="w-full bg-gray-50 dark:bg-[#020617] flex flex-col font-sans relative pb-12 transition-colors duration-300"')
content = content.replace('bg-white rounded-3xl shadow-lg border border-gray-100', 'bg-white dark:bg-[#0F172A] rounded-3xl shadow-lg border border-gray-200 dark:border-white/10')
content = content.replace('text-gray-900 tracking-tight', 'text-gray-900 dark:text-white tracking-tight')

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
