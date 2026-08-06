import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Replace initial render logic in the AdminTreeNode
old_render = """        <div className="h-12 w-12 rounded-full bg-gradient-to-br from-[#0F172A] to-[#0F172A] flex items-center justify-center font-bold text-lg text-gray-900 dark:text-white shadow-inner border border-gray-200 dark:border-white/10">
          {node.displayName.charAt(0).toUpperCase()}
        </div>"""

new_render = """        <div className="h-12 w-12 rounded-full bg-gradient-to-br from-[#0F172A] to-[#0F172A] flex items-center justify-center font-bold text-lg text-gray-900 dark:text-white shadow-inner border border-gray-200 dark:border-white/10 overflow-hidden">
          {(node.profileImage || node.avatarUrl) ? (
            <img src={node.profileImage || node.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
          ) : (
            node.displayName?.charAt(0).toUpperCase() || 'U'
          )}
        </div>"""

content = content.replace(old_render, new_render)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
