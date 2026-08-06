import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    'className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-[#1E3A8A]/30 rounded-full blur-[120px] pointer-events-none mix-blend-screen"',
    'className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-blue-400/10 dark:bg-blue-900/30 rounded-full blur-[120px] pointer-events-none"'
)
content = content.replace(
    'className="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] bg-[#EF4444]/20 rounded-full blur-[150px] pointer-events-none mix-blend-screen"',
    'className="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] bg-red-400/10 dark:bg-red-900/20 rounded-full blur-[150px] pointer-events-none"'
)

with open('src/App.tsx', 'w') as f:
    f.write(content)
