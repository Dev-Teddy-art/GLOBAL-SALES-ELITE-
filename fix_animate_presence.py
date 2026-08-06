import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Add AnimatePresence import
if "AnimatePresence" not in content:
    content = content.replace("import { motion } from 'motion/react';", "import { motion, AnimatePresence } from 'motion/react';")

old_payout_body_start = '''          <tbody className="divide-y divide-gray-100 text-gray-700">'''
new_payout_body_start = '''          <tbody className="divide-y divide-gray-100 text-gray-700">
            <AnimatePresence>'''
content = content.replace(old_payout_body_start, new_payout_body_start)

old_payout_body_end = '''            {users.filter(u => u.role !== 'admin' && u.bankAccountNumber).length === 0 && ('''
new_payout_body_end = '''            </AnimatePresence>
            {users.filter(u => u.role !== 'admin' && u.bankAccountNumber).length === 0 && ('''
content = content.replace(old_payout_body_end, new_payout_body_end)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
