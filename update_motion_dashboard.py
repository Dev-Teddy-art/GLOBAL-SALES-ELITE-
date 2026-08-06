import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

if "import { motion }" not in content:
    content = content.replace("import { ReferralTree } from './ReferralTree';", "import { ReferralTree } from './ReferralTree';\nimport { motion } from 'motion/react';")

# Dashboard cards to animate
content = content.replace('<div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">', '<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">', 1)
content = content.replace('<div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8 relative overflow-hidden">', '<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8 relative overflow-hidden">', 1)

# Find Network Section and add motion
network_section = '        {/* Network Section */}\n        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">'
new_network_section = '        {/* Network Section */}\n        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.3 }} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">'
content = content.replace(network_section, new_network_section)

# Find CommissionCalculator component and add motion inside it
calc_div = '<div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">'
new_calc_div = '<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.4 }} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">'
# Replace the first occurrence in the file (which is in CommissionCalculator)
content = content.replace(calc_div, new_calc_div, 1)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
