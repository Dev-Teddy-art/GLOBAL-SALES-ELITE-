import re

with open('src/components/ReferralTree.tsx', 'r') as f:
    content = f.read()

# Replace the initial render logic in the TreeNode
old_render = """            <div className={`h-10 w-10 rounded-full flex-shrink-0 flex items-center justify-center font-bold text-sm ${node.isAdmin || node.role === 'admin' ? 'bg-[#EF4444]/10 text-[#EF4444]' : 'bg-gray-100 dark:bg-[#0F172A] text-[#0F172A] dark:text-white'}`}>
              {node.isAdmin || node.role === 'admin' ? <Shield size={18} /> : node.displayName.charAt(0).toUpperCase()}
            </div>"""

new_render = """            <div className={`h-10 w-10 rounded-full flex-shrink-0 flex items-center justify-center font-bold text-sm overflow-hidden ${node.isAdmin || node.role === 'admin' ? 'bg-[#EF4444]/10 text-[#EF4444]' : 'bg-gray-100 dark:bg-[#0F172A] text-[#0F172A] dark:text-white'}`}>
              {(node.profileImage || node.avatarUrl) ? (
                <img src={node.profileImage || node.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
              ) : (node.isAdmin || node.role === 'admin') ? (
                <Shield size={18} />
              ) : (
                node.displayName?.charAt(0).toUpperCase() || 'U'
              )}
            </div>"""

content = content.replace(old_render, new_render)

with open('src/components/ReferralTree.tsx', 'w') as f:
    f.write(content)
