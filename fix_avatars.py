import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

avatars_old = """              <div className="flex -space-x-4">
                {[1,2,3,4].map(i => (
                  <div key={i} className={`w-12 h-12 rounded-full border-2 border-[#0B0F19] bg-gradient-to-br from-red-500 to-red-900 flex items-center justify-center font-bold text-white text-xs z-${10-i}`}>
                    +{i}k
                  </div>
                ))}
              </div>
              <span className="text-gray-500 text-sm font-bold uppercase tracking-widest">Active Earners</span>"""

avatars_new = """              <div className="flex -space-x-4">
                <div className="w-12 h-12 rounded-full border-2 border-white dark:border-[#0B0F19] bg-gradient-to-br from-blue-500 to-blue-900 flex items-center justify-center font-bold text-white text-xs z-10 shadow-lg">
                  <Users size={20} />
                </div>
              </div>
              <span className="text-gray-500 text-sm font-bold uppercase tracking-widest">Network Earners</span>"""

content = content.replace(avatars_old, avatars_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)
