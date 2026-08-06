import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Fix the min-h-screen container for SignUpPage
# Old: <div className="min-h-screen bg-gray-50 dark:bg-gray-50 dark:bg-[#0F172A] flex flex-col items-center justify-center p-6 py-12 relative font-sans">
# New: <div className="min-h-screen bg-gray-50 dark:bg-[#0F172A] flex flex-col items-center p-6 pt-24 pb-12 relative font-sans">
content = content.replace(
    '<div className="min-h-screen bg-gray-50 dark:bg-gray-50 dark:bg-[#0F172A] flex flex-col items-center justify-center p-6 py-12 relative font-sans">',
    '<div className="min-h-screen bg-gray-50 dark:bg-[#0F172A] flex flex-col items-center p-6 pt-24 pb-12 relative font-sans overflow-y-auto">'
)

with open('src/App.tsx', 'w') as f:
    f.write(content)
