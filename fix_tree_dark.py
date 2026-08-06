import re

with open('src/components/ReferralTree.tsx', 'r') as f:
    content = f.read()

content = re.sub(r'\bbg-white\b', 'bg-white dark:bg-[#1E293B]', content)
content = re.sub(r'\bbg-gray-50\b', 'bg-gray-50 dark:bg-white/5', content)
content = re.sub(r'\bborder-gray-100\b', 'border-gray-100 dark:border-white/10', content)
content = re.sub(r'\bborder-gray-200\b', 'border-gray-200 dark:border-white/10', content)
content = re.sub(r'\btext-gray-900\b', 'text-gray-900 dark:text-white', content)
content = re.sub(r'\btext-gray-700\b', 'text-gray-700 dark:text-gray-200', content)
content = re.sub(r'\btext-gray-500\b', 'text-gray-500 dark:text-gray-400', content)
content = re.sub(r'\btext-gray-400\b', 'text-gray-400 dark:text-gray-500', content)
content = re.sub(r'\bfrom-gray-200\b', 'from-gray-200 dark:from-white/20', content)

with open('src/components/ReferralTree.tsx', 'w') as f:
    f.write(content)
