import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

old_render = """                    <div className="w-10 h-10 rounded-full bg-[#10B981]/10 flex items-center justify-center text-[#10B981]">
                      <Landmark size={20} />
                    </div>"""

new_render = """                    <div className="w-10 h-10 rounded-full bg-[#10B981]/10 flex items-center justify-center text-[#10B981] overflow-hidden">
                      {(w.userRef?.profileImage || w.userRef?.avatarUrl) ? (
                        <img src={w.userRef?.profileImage || w.userRef?.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
                      ) : (
                        <Landmark size={20} />
                      )}
                    </div>"""

content = content.replace(old_render, new_render)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
