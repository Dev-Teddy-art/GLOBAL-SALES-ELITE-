import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Replace hardcoded dark colors
content = content.replace('bg-[#020617]', 'bg-gray-50 dark:bg-[#020617]')
content = content.replace('text-gray-200', 'text-gray-900 dark:text-gray-200')
content = content.replace('bg-[#0F172A]/50', 'bg-white/80 dark:bg-[#0F172A]/50')
content = content.replace('bg-[#0F172A]/80', 'bg-white/90 dark:bg-[#0F172A]/80')
content = content.replace('bg-[#1E293B]', 'bg-white dark:bg-[#1E293B]')
content = content.replace('bg-[#1E293B]/80', 'bg-white/80 dark:bg-[#1E293B]/80')
content = content.replace('border-white/5', 'border-gray-200 dark:border-white/5')
content = content.replace('border-white/10', 'border-gray-200 dark:border-white/10')
content = content.replace('border-white/20', 'border-gray-300 dark:border-white/20')
content = content.replace('text-white', 'text-gray-900 dark:text-white')
content = content.replace('text-gray-300', 'text-gray-700 dark:text-gray-300')
content = content.replace('text-gray-400', 'text-gray-600 dark:text-gray-400')
content = content.replace('text-gray-500', 'text-gray-500 dark:text-gray-500')
content = content.replace('bg-black/20', 'bg-gray-100 dark:bg-black/20')
content = content.replace('bg-black/30', 'bg-gray-100 dark:bg-black/30')
content = content.replace('bg-black/60', 'bg-black/40 dark:bg-black/60')

# Also add ThemeToggle
if 'import { ThemeToggle }' not in content:
    content = content.replace("import { motion, AnimatePresence } from 'motion/react';", "import { motion, AnimatePresence } from 'motion/react';\nimport { ThemeToggle } from './ThemeToggle';")

if '<ThemeToggle />' not in content:
    content = content.replace('<button \n              onClick={() => navigate(\'/dashboard\')}', '<ThemeToggle className="text-gray-900 dark:text-gray-300" />\n            <button \n              onClick={() => navigate(\'/dashboard\')}')

# Don't accidentally replace the newly added text-gray-900 dark:text-white incorrectly.
with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
