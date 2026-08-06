import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("""            <div className="text-white font-black text-xl tracking-tighter flex items-center gap-2">
              <span className="bg-[#EF4444] p-1.5 rounded-lg"><Network size={20} className="text-white" /></span>
              GSE
            </div>""", """            <Logo />""")

content = content.replace("""            <div className="text-white font-black text-2xl tracking-tighter flex items-center gap-2 mb-4">
              <span className="bg-[#EF4444] p-1.5 rounded-lg"><Network size={20} className="text-white" /></span>
              Global Sales Elite
            </div>""", """            <Logo className="mb-4" />""")

with open('src/App.tsx', 'w') as f:
    f.write(content)
