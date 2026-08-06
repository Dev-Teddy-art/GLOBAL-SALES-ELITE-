import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

old_link = 'const link = `${window.location.origin}/signup?ref=${profile?.referralCode}`;'
new_link = 'const refString = profile?.firstName ? `${profile.firstName.replace(/\\s+/g, "")}-${profile.referralCode}` : profile?.referralCode;\n    const link = `${window.location.origin}/signup?ref=${refString}`;'
content = content.replace(old_link, new_link)

old_input = 'value={`${window.location.origin}/signup?ref=${profile?.referralCode}`}'
new_input = 'value={`${window.location.origin}/signup?ref=${profile?.firstName ? `${profile.firstName.replace(/\\s+/g, "")}-${profile.referralCode}` : profile?.referralCode}`}'
content = content.replace(old_input, new_input)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
