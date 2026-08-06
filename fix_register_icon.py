import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_register = """          <div className="text-center mb-2">
            <Logo className="h-16 md:h-20 mx-auto mb-6 justify-center" />
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Create an Account</h2>"""

new_register = """          <div className="text-center mb-2">
            <div className="mx-auto bg-[#EF4444] p-3 rounded-2xl w-max mb-4 shadow-lg">
              <UserPlus size={24} className="text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Create an Account</h2>"""

content = content.replace(old_register, new_register)

with open('src/App.tsx', 'w') as f:
    f.write(content)
