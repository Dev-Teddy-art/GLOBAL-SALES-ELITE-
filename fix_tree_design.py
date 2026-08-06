import re

with open('src/components/ReferralTree.tsx', 'r') as f:
    content = f.read()

# Make the tree card look more premium
content = content.replace(
    'className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden"', 
    'className="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden relative"'
)

# Header of tree
content = content.replace(
    'className="p-6 border-b border-gray-100 bg-gray-50/50"',
    'className="p-6 md:p-8 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white relative z-10"'
)

# Node Card
content = content.replace(
    'className="flex-1 bg-white border border-gray-200 rounded-xl p-3 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group"',
    'className="flex-1 bg-white border border-gray-100 rounded-2xl p-4 flex items-center gap-4 shadow-sm hover:shadow-md transition-all hover:-translate-y-0.5 relative overflow-hidden group"'
)

# Line colors
content = content.replace(
    'bg-gray-200',
    'bg-gradient-to-b from-gray-200 to-transparent'
)

# Badge for role
content = content.replace(
    'className="text-[10px] uppercase tracking-wider font-bold bg-amber-100 text-amber-700 px-2 py-0.5 rounded"',
    'className="text-[10px] uppercase tracking-widest font-bold bg-amber-100 text-amber-700 px-2.5 py-1 rounded-full"'
)

with open('src/components/ReferralTree.tsx', 'w') as f:
    f.write(content)
