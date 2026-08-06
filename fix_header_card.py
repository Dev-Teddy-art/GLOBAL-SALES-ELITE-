import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

old_header = '<div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8 flex flex-col md:flex-row gap-6 justify-between items-start md:items-center">'
new_header = '<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8 flex flex-col md:flex-row gap-6 justify-between items-start md:items-center">'

content = content.replace(old_header, new_header)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
