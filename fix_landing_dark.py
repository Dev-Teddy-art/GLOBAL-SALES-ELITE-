with open('src/App.tsx', 'r') as f:
    content = f.read()

# Replace hardcoded text colors in App.tsx for LandingPage
content = content.replace('text-white', 'text-gray-900 dark:text-white')
# some places it might break, e.g. text-white in buttons. Let's fix that.
content = content.replace('bg-[#EF4444] text-gray-900 dark:text-white', 'bg-[#EF4444] text-white')
content = content.replace('text-gray-900 dark:text-white/80', 'text-gray-600 dark:text-white/80')
content = content.replace('text-gray-900 dark:text-white/50', 'text-gray-500 dark:text-white/50')
content = content.replace('text-gray-400', 'text-gray-600 dark:text-gray-400')
content = content.replace('bg-white/5', 'bg-white dark:bg-white/5')
content = content.replace('border-white/10', 'border-gray-200 dark:border-white/10')
content = content.replace('bg-black/40', 'bg-gray-200 dark:bg-black/40')
content = content.replace('bg-black/30', 'bg-white dark:bg-black/30')
content = content.replace('bg-black/20', 'bg-white dark:bg-black/20')
content = content.replace('bg-[#1E293B]/80', 'bg-white/80 dark:bg-[#1E293B]/80')
content = content.replace('bg-[#1E293B]', 'bg-white dark:bg-[#1E293B]')
content = content.replace('border-white/5', 'border-gray-100 dark:border-white/5')

# Also fix the text in buttons that might have been changed by mistake
content = content.replace('text-gray-900 dark:text-white font-bold', 'text-white font-bold')

with open('src/App.tsx', 'w') as f:
    f.write(content)
