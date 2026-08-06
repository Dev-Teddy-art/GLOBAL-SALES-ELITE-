import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { ThemeToggle } from './ThemeToggle';", "import { ThemeToggle } from './ThemeToggle';\nimport { ProfilePhotoUpload } from './ProfilePhotoUpload';")

# Replace header in Dashboard
header_find = """            <div className="flex flex-col items-end hidden sm:flex">
              <span className="font-semibold text-sm">{profile.displayName}</span>
              <span className="text-xs text-white/70 uppercase tracking-widest">{profile.role}</span>
            </div>
            <button"""

header_replace = """            <div className="flex flex-col items-end hidden sm:flex">
              <span className="font-semibold text-sm">{profile.displayName}</span>
              <span className="text-xs text-white/70 uppercase tracking-widest">{profile.role}</span>
            </div>
            <ProfilePhotoUpload />
            <button"""

content = content.replace(header_find, header_replace)

# Also update the Welcome header if applicable
welcome_find = """            <h2 className="text-3xl md:text-4xl font-black mb-2 tracking-tight drop-shadow-sm">
              {isFirstLogin ? 'Welcome' : 'Welcome back'}, <span className="text-[#e03126]">{profile.firstName || profile.displayName?.split(' ')[0]}</span>
            </h2>"""

welcome_replace = """            <div className="flex items-center gap-6 mb-2">
              <ProfilePhotoUpload className="w-16 h-16 sm:w-20 sm:h-20 text-xl" />
              <h2 className="text-3xl md:text-4xl font-black tracking-tight drop-shadow-sm">
                {isFirstLogin ? 'Welcome' : 'Welcome back'}, <span className="text-[#e03126]">{profile.firstName || profile.displayName?.split(' ')[0]}</span>
              </h2>
            </div>"""

content = content.replace(welcome_find, welcome_replace)

# Oh wait, ProfilePhotoUpload uses fixed w-10 h-10 right now. Let's make it accept dynamic w-h if className has it, or just keep it simple.
# Wait, ProfilePhotoUpload has hardcoded w-10 h-10! Let's update ProfilePhotoUpload to use className correctly.

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)

