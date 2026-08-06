import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Add id to AdminDashboardTable root div
old_admin_root = '    <div className="overflow-x-auto bg-white rounded-xl border border-gray-100 shadow-sm">'
new_admin_root = '    <div id="admin-console" className="overflow-x-auto bg-white rounded-xl border border-gray-100 shadow-sm">'
content = content.replace(old_admin_root, new_admin_root)

# Update Admin Console button
old_button = '''              <button className="text-sm font-semibold text-amber-200 hover:text-amber-100 transition-colors bg-white/10 px-3 py-1.5 rounded mr-2 hidden sm:block">
                Admin Console
              </button>'''

new_button = '''              <button onClick={() => document.getElementById('admin-console')?.scrollIntoView({ behavior: 'smooth' })} className="text-sm font-semibold text-amber-200 hover:text-amber-100 transition-colors bg-white/10 px-3 py-1.5 rounded mr-2 hidden sm:block">
                Admin Console
              </button>'''

content = content.replace(old_button, new_button)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
