import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

old_render = """                  <td className="py-3 px-4 text-sm font-bold text-gray-900 dark:text-white">
                    {s.userRef?.displayName || 'Unknown'}
                  </td>"""

new_render = """                  <td className="py-3 px-4 text-sm font-bold text-gray-900 dark:text-white">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-gray-200 dark:bg-[#0F172A] flex items-center justify-center text-[10px] overflow-hidden flex-shrink-0">
                        {(s.userRef?.profileImage || s.userRef?.avatarUrl) ? (
                          <img src={s.userRef?.profileImage || s.userRef?.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
                        ) : (
                          (s.userRef?.displayName?.charAt(0).toUpperCase() || 'U')
                        )}
                      </div>
                      {s.userRef?.displayName || 'Unknown'}
                    </div>
                  </td>"""

content = content.replace(old_render, new_render)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
