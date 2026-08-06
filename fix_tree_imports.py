import re

with open('src/components/ReferralTree.tsx', 'r') as f:
    content = f.read()

if "import { motion }" not in content and "import { motion," not in content:
    content = content.replace("import { ChevronRight, ChevronDown, User as UserIcon, Search, Shield } from 'lucide-react';", "import { ChevronRight, ChevronDown, User as UserIcon, Search, Shield } from 'lucide-react';\nimport { motion, AnimatePresence } from 'motion/react';")

with open('src/components/ReferralTree.tsx', 'w') as f:
    f.write(content)
