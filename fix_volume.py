import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace('<div className="text-blue-400 font-mono font-bold">Dynamic</div>', '<div className="text-blue-400 font-mono font-bold">{networkSize !== null ? `₦${((networkSize) * 50000).toLocaleString()}` : "..."}</div>')

with open('src/App.tsx', 'w') as f:
    f.write(content)
