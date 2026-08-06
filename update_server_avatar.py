import re

with open('server.ts', 'r') as f:
    content = f.read()

# In signup extraData, include avatarUrl
content = content.replace(
    "bankName: extraData.bankName || '',",
    "bankName: extraData.bankName || '',\n        avatarUrl: extraData.avatarUrl || '',"
)

# Add update-avatar endpoint
new_endpoint = """
  app.post('/api/auth/update-avatar', async (req, res) => {
    try {
      const { userId, avatarUrl } = req.body;
      const updatedUser = await sanityClient.patch(userId)
        .set({ avatarUrl })
        .commit();
      res.json({ user: updatedUser });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });
"""

content = content.replace("  app.post('/api/sanity/query',", new_endpoint + "\n  app.post('/api/sanity/query',")

with open('server.ts', 'w') as f:
    f.write(content)
