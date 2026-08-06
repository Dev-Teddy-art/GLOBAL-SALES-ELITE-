import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Import
content = content.replace("import { Logo } from './components/Logo';", "import { Logo } from './components/Logo';\nimport { AvatarSelector } from './components/AvatarSelector';")

# State
content = content.replace(
    "bankName: ''\n  });",
    "bankName: '',\n    avatarUrl: 'https://api.dicebear.com/9.x/avataaars-neutral/svg?seed=Felix&backgroundColor=e2e8f0'\n  });"
)

# Form output
form_html = """            <div className="flex flex-col gap-2 text-left">
              <label className="text-gray-600 dark:text-gray-700 dark:text-white/80 text-sm font-medium pl-1">Bank Account Name *</label>
              <input required type="text" name="bankAccountName" value={formData.bankAccountName} onChange={handleChange} className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/20 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444]" />
            </div>"""

new_form_html = form_html + """
            <div className="flex flex-col gap-2 text-left mb-2">
              <AvatarSelector value={formData.avatarUrl} onChange={(val) => setFormData(prev => ({...prev, avatarUrl: val}))} />
            </div>"""

content = content.replace(form_html, new_form_html)

with open('src/App.tsx', 'w') as f:
    f.write(content)
