import re

with open('server.ts', 'r') as f:
    content = f.read()

# Replace update-avatar to also unset profileImage
old = """      const updatedUser = await sanityClient.patch(userId)
        .set({ avatarUrl })
        .commit();"""

new = """      const updatedUser = await sanityClient.patch(userId)
        .set({ avatarUrl })
        .unset(['profileImage'])
        .commit();"""

content = content.replace(old, new)

with open('server.ts', 'w') as f:
    f.write(content)
