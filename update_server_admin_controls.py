import re

with open('server.ts', 'r') as f:
    content = f.read()

admin_endpoints = """
  app.post('/api/admin/update-user', async (req, res) => {
    try {
      const { adminId, userId, updates } = req.body;
      const admin = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: adminId });
      if (!admin || (admin.role !== 'admin' && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      
      const updatedUser = await sanityClient.patch(userId)
        .set(updates)
        .commit();
        
      res.json({ success: true, user: updatedUser });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/api/admin/ban-user', async (req, res) => {
    try {
      const { adminId, userId, banned } = req.body;
      const admin = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: adminId });
      if (!admin || (admin.role !== 'admin' && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      
      const updatedUser = await sanityClient.patch(userId)
        .set({ status: banned ? 'banned' : 'active' })
        .commit();
        
      res.json({ success: true, user: updatedUser });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });
"""

content = content.replace("  app.post('/api/admin/fix-nested-sets',", admin_endpoints + "\n  app.post('/api/admin/fix-nested-sets',")

with open('server.ts', 'w') as f:
    f.write(content)
