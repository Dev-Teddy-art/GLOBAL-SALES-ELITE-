import re

with open('src/components/Navbar.tsx', 'r') as f:
    content = f.read()

# Add ThemeToggle import
content = content.replace("import { useAuth } from '../contexts/AuthContext';", "import { useAuth } from '../contexts/AuthContext';\nimport { ThemeToggle } from './ThemeToggle';")

# Update header wrapper
old_header = '<header className="bg-[#0F172A] text-white shadow-md relative z-50">'
new_header = '<header className="bg-white dark:bg-[#0F172A] border-b border-gray-200 dark:border-white/10 shadow-sm relative z-50 transition-colors">'
content = content.replace(old_header, new_header)

# Update Logo text color
content = content.replace('h-10 w-auto bg-white/10 rounded px-2', 'h-10 w-auto bg-gray-100 dark:bg-white/10 rounded px-2')
content = content.replace('text-xl font-bold tracking-wider hidden sm:block', 'text-xl font-bold tracking-wider hidden sm:block text-gray-900 dark:text-white')

# Update admin button
old_admin_btn = 'className="text-white/80 hover:text-white hover:bg-white/10 p-2 rounded-xl transition-colors flex items-center gap-2 text-sm font-bold"'
new_admin_btn = 'className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/10 p-2 rounded-xl transition-colors flex items-center gap-2 text-sm font-bold"'
content = content.replace(old_admin_btn, new_admin_btn)

# Update bell button
old_bell = 'className="relative p-2 text-white/80 hover:text-white hover:bg-white/10 rounded-xl transition-colors"'
new_bell = 'className="relative p-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/10 rounded-xl transition-colors"'
content = content.replace(old_bell, new_bell)

# Add theme toggle
old_bell_full = """          <button onClick={handleOpenNotifications} className="relative p-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/10 rounded-xl transition-colors">
            <Bell size={20} />
            {unreadCount > 0 && (
              <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-[#EF4444] rounded-full border-2 border-[#0F172A]" />
            )}
          </button>"""
new_bell_full = """          <ThemeToggle className="text-gray-600 dark:text-gray-300 mr-2" />
          
          <button onClick={handleOpenNotifications} className="relative p-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/10 rounded-xl transition-colors">
            <Bell size={20} />
            {unreadCount > 0 && (
              <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-[#EF4444] rounded-full border-2 border-white dark:border-[#0F172A]" />
            )}
          </button>"""
content = content.replace(old_bell_full, new_bell_full)

# Update avatar placeholder
content = content.replace('w-10 h-10 rounded-full bg-white/10 border-2 border-white/20 flex items-center justify-center font-bold overflow-hidden', 'w-10 h-10 rounded-full bg-gray-100 dark:bg-white/10 border-2 border-gray-200 dark:border-white/20 flex items-center justify-center font-bold text-gray-900 dark:text-white overflow-hidden')

# Update sign out button
old_signout = 'className="text-white/80 hover:text-[#EF4444] hover:bg-white/10 p-2 rounded-xl transition-colors hidden md:block"'
new_signout = 'className="text-gray-600 dark:text-gray-300 hover:text-[#EF4444] dark:hover:text-[#EF4444] hover:bg-gray-100 dark:hover:bg-white/10 p-2 rounded-xl transition-colors hidden md:block"'
content = content.replace(old_signout, new_signout)

with open('src/components/Navbar.tsx', 'w') as f:
    f.write(content)
