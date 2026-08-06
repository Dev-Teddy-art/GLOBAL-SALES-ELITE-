import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

old_render = """            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 + 0.3 }}
              key={u.id || i} 
              className="flex gap-3 items-start"
            >
              <div className="mt-0.5 w-2 h-2 rounded-full flex-shrink-0 bg-[#0F172A]" />
              <div>
                <p className="text-sm text-gray-700 dark:text-gray-300 leading-tight">New user registration: {u.displayName}</p>
                <span className="text-xs text-gray-500 dark:text-gray-500">{new Date(u.createdAt || Date.now()).toLocaleDateString()}</span>
              </div>
            </motion.div>"""

new_render = """            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 + 0.3 }}
              key={u.id || i} 
              className="flex gap-3 items-start p-2 hover:bg-gray-50 dark:hover:bg-white/5 rounded-xl transition-colors"
            >
              <div className="w-8 h-8 rounded-full flex-shrink-0 bg-gray-200 dark:bg-[#0F172A] flex items-center justify-center text-xs overflow-hidden font-bold">
                {(u.profileImage || u.avatarUrl) ? (
                  <img src={u.profileImage || u.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
                ) : (
                  (u.displayName?.charAt(0).toUpperCase() || 'U')
                )}
              </div>
              <div className="pt-0.5">
                <p className="text-sm font-bold text-gray-900 dark:text-gray-200 leading-tight">New user joined</p>
                <p className="text-xs text-gray-700 dark:text-gray-400 mt-0.5">{u.displayName}</p>
                <span className="text-[10px] text-gray-500 block mt-1">{new Date(u.createdAt || Date.now()).toLocaleDateString()}</span>
              </div>
            </motion.div>"""

content = content.replace(old_render, new_render)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
