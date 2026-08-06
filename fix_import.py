import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { Logo } from './Logo';", "import { Logo } from './Logo';\nimport { ProfilePhotoUpload } from './ProfilePhotoUpload';")

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
