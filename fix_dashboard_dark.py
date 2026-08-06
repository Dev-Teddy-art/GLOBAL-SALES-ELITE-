import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Replace colors safely using word boundaries
content = re.sub(r'\bbg-gray-50\b', 'bg-gray-50 dark:bg-[#0B0F19]', content)
content = re.sub(r'\bbg-white\b', 'bg-white dark:bg-[#1E293B]', content)
content = re.sub(r'\btext-gray-900\b', 'text-gray-900 dark:text-white', content)
content = re.sub(r'\btext-gray-800\b', 'text-gray-800 dark:text-gray-100', content)
content = re.sub(r'\btext-gray-700\b', 'text-gray-700 dark:text-gray-200', content)
content = re.sub(r'\btext-gray-600\b', 'text-gray-600 dark:text-gray-300', content)
content = re.sub(r'\btext-gray-500\b', 'text-gray-500 dark:text-gray-400', content)
content = re.sub(r'\btext-gray-400\b', 'text-gray-400 dark:text-gray-500', content)
content = re.sub(r'\bborder-gray-100\b', 'border-gray-100 dark:border-white/10', content)
content = re.sub(r'\bborder-gray-200\b', 'border-gray-200 dark:border-white/10', content)
content = re.sub(r'\bbg-gray-100\b', 'bg-gray-100 dark:bg-white/10', content)
content = re.sub(r'\bbg-blue-50\b', 'bg-blue-50 dark:bg-blue-900/20', content)
content = re.sub(r'\bbg-red-50\b', 'bg-red-50 dark:bg-red-900/20', content)
content = re.sub(r'\bbg-amber-50\b', 'bg-amber-50 dark:bg-amber-900/20', content)
content = re.sub(r'\bborder-blue-100\b', 'border-blue-100 dark:border-blue-900/30', content)
content = re.sub(r'\bborder-red-100\b', 'border-red-100 dark:border-red-900/30', content)
content = re.sub(r'\bborder-amber-100\b', 'border-amber-100 dark:border-amber-900/30', content)

# But wait! I had already modified it using simple replace. Let's reset Dashboard.tsx from git first, but we didn't use git.
