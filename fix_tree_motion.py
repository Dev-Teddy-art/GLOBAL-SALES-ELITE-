import re

with open('src/components/ReferralTree.tsx', 'r') as f:
    content = f.read()

old_node = '<div className="flex-1 bg-white border border-gray-200 rounded-xl p-3 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">'
new_node = '<motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.3 }} className="flex-1 bg-white border border-gray-200 rounded-xl p-3 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">'

content = content.replace(old_node, new_node)

with open('src/components/ReferralTree.tsx', 'w') as f:
    f.write(content)
