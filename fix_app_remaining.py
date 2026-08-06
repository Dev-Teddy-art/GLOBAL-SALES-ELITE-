with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace('bg-[#070b5e]', 'bg-gray-50 dark:bg-[#070b5e]')
# Let's fix the SignUpPage text colors!
content = content.replace('text-white/70', 'text-gray-600 dark:text-white/70')
content = content.replace('text-white/80', 'text-gray-700 dark:text-white/80')
content = content.replace('text-white/50', 'text-gray-500 dark:text-white/50')
content = content.replace('text-white/40', 'text-gray-400 dark:text-white/40')

# Also, if we have "bg-white/10 backdrop-blur-md" in SignUpPage
content = content.replace('bg-white/10 backdrop-blur-md', 'bg-white dark:bg-white/10 backdrop-blur-md')
content = content.replace('border-white/20', 'border-gray-200 dark:border-white/20')
# Inside forms:
content = content.replace('bg-white/5 border', 'bg-gray-100 dark:bg-white/5 border')

with open('src/App.tsx', 'w') as f:
    f.write(content)
