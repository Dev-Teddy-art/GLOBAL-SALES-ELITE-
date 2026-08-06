import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

old_btn = """              <button 
                onClick={copyReferralLink}
                className="bg-[#EF4444] hover:bg-[#c9291f] text-white p-3 rounded-xl transition-colors shadow-lg hover:shadow-xl hover:-translate-y-0.5 duration-200"
              >
                <Copy size={18} />
              </button>"""

new_btn = """              <button 
                onClick={copyReferralLink}
                className="bg-[#EF4444] hover:bg-[#c9291f] text-white px-4 py-3 rounded-xl transition-colors shadow-lg hover:shadow-xl hover:-translate-y-0.5 duration-200 flex items-center gap-2 font-bold text-sm"
              >
                <Copy size={16} /> Copy
              </button>"""

content = content.replace(old_btn, new_btn)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
