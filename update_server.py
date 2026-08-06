import re

with open('server.ts', 'r') as f:
    content = f.read()

new_endpoint = """
  app.post('/api/auth/update-profile-image', express.json({limit: '10mb'}), async (req, res) => {
    try {
      const { userId, imageBase64 } = req.body;
      
      const base64Data = imageBase64.replace(/^data:image\/\w+;base64,/, "");
      const buffer = Buffer.from(base64Data, 'base64');
      
      const asset = await sanityClient.assets.upload('image', buffer, {
        filename: 'profile-' + userId + '.jpg'
      });
      
      const updatedUser = await sanityClient.patch(userId)
        .set({ profileImage: asset.url })
        .commit();
        
      res.json({ url: asset.url, user: updatedUser });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });
"""

# Insert before app.post('/api/sanity/query'
content = content.replace("  app.post('/api/sanity/query',", new_endpoint + "\n  app.post('/api/sanity/query',")
# Also need to increase express.json limit globally if it's there
content = content.replace("app.use(express.json());", "app.use(express.json({ limit: '10mb' }));")

with open('server.ts', 'w') as f:
    f.write(content)
