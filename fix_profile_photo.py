import re

with open('src/components/ProfilePhotoUpload.tsx', 'r') as f:
    content = f.read()

# Replace hardcoded w-10 h-10 with something that checks className
# Since we passed w-16 h-16 in className, let's remove w-10 h-10 from the inner div and add className to the inner div, or just pass it in.

content = content.replace(
    '<div className={`relative group cursor-pointer ${className}`} onClick={() => fileInputRef.current?.click()}>',
    '<div className={`relative group cursor-pointer ${className || "w-10 h-10"}`} onClick={() => fileInputRef.current?.click()}>'
)

content = content.replace(
    'className="w-10 h-10 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-800 border-2 border-white/20 flex items-center justify-center text-gray-700 dark:text-gray-300 font-bold shadow-sm relative"',
    'className="w-full h-full rounded-full overflow-hidden bg-gray-200 dark:bg-gray-800 border-2 border-white/20 flex items-center justify-center text-gray-700 dark:text-gray-300 font-bold shadow-sm relative"'
)

with open('src/components/ProfilePhotoUpload.tsx', 'w') as f:
    f.write(content)
