import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Fix Inputs in Earnings Calculator
content = content.replace('bg-gray-50 border border-gray-200 text-gray-900 rounded-xl', 'bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 text-gray-900 dark:text-white rounded-xl')
content = content.replace('focus:ring-[#0F172A]', 'focus:ring-[#0F172A] dark:focus:ring-white/20')

# Also in "Log a Sale" section
content = content.replace('className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3.5', 'className="w-full bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 text-gray-900 dark:text-white rounded-xl px-4 py-3.5')

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)

