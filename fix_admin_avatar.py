import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

old_avatar = """        <div className="h-12 w-12 rounded-full bg-gradient-to-br from-[#0F172A] to-[#0F172A] flex items-center justify-center font-bold text-lg text-white shadow-inner border border-gray-200 dark:border-white/10 overflow-hidden">
          {(node.profileImage || node.avatarUrl) ? (
            <img src={node.profileImage || node.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
          ) : (
            node.displayName?.charAt(0).toUpperCase() || 'U'
          )}
        </div>"""

new_avatar = """        <div className={`h-12 w-12 rounded-full bg-gradient-to-br ${node.isAdmin || node.role === 'admin' ? 'from-[#EF4444]/20 to-[#EF4444]/10 text-[#EF4444]' : 'from-[#0F172A] to-[#0F172A] text-white'} flex items-center justify-center font-bold text-lg shadow-inner border border-gray-200 dark:border-white/10 overflow-hidden`}>
          {(node.profileImage || node.avatarUrl) ? (
            <img src={node.profileImage || node.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
          ) : (node.isAdmin || node.role === 'admin') ? (
            <Crown size={20} />
          ) : (
            node.displayName?.charAt(0).toUpperCase() || 'U'
          )}
        </div>"""

content = content.replace(old_avatar, new_avatar)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
