import re

with open('server.ts', 'r') as f:
    content = f.read()

# Replace update-profile-image to also unset avatarUrl
old = """      const updatedUser = await sanityClient.patch(userId)
        .set({ profileImage: asset.url })
        .commit();"""

new = """      const updatedUser = await sanityClient.patch(userId)
        .set({ profileImage: asset.url })
        .unset(['avatarUrl'])
        .commit();"""

content = content.replace(old, new)

with open('server.ts', 'w') as f:
    f.write(content)
