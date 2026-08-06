import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Make sure Navbar is imported
if "import { Navbar }" not in content:
    content = content.replace("import { Logo } from './Logo';", "import { Logo } from './Logo';\nimport { Navbar } from './Navbar';")

# Find the header block
header_regex = re.compile(r'<header className="bg-\[#0F172A\].*?</header>', re.DOTALL)
content = header_regex.sub('<Navbar />', content)

# Remove local handleOpenNotifications and showNotifications state if not needed elsewhere
# Actually, they might be referenced elsewhere, but let's just leave them or let TS complain
content = re.sub(r'const \[showNotifications, setShowNotifications\] = useState\(false\);\n', '', content)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
