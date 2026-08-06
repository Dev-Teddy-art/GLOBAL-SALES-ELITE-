import re

with open('server.ts', 'r') as f:
    content = f.read()

new_endpoint = '''
  app.post('/api/admin/fix-nested-sets', async (req, res) => {
    try {
      // Fetch all users
      const users = await sanityClient.fetch(`*[_type == "user"]`);
      
      // Build tree
      const tree: Record<string, any[]> = {};
      users.forEach((u: any) => {
        const parentId = u.sponsorId || 'admin';
        if (!tree[parentId]) tree[parentId] = [];
        tree[parentId].push(u);
      });

      // Traverse and assign lft/rgt
      let counter = 1;
      const updates: any[] = [];
      
      function traverse(nodeId: string) {
        const lft = counter++;
        const children = tree[nodeId] || [];
        for (const child of children) {
          traverse(child._id);
        }
        const rgt = counter++;
        
        if (nodeId !== 'admin') {
          updates.push({ id: nodeId, lft, rgt });
        }
      }
      
      traverse('admin');
      
      // We can use a transaction, but if there are many users, we should chunk it.
      // For simplicity, we just do one transaction assuming small number of users.
      const transaction = sanityClient.transaction();
      for (const update of updates) {
        transaction.patch(update.id, p => p.set({ lft: update.lft, rgt: update.rgt }));
      }
      
      await transaction.commit();
      
      res.json({ message: `Successfully updated nested sets for ${updates.length} users.` });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  if (process.env.NODE_ENV !== "production") {'''

content = content.replace('  if (process.env.NODE_ENV !== "production") {', new_endpoint)

with open('server.ts', 'w') as f:
    f.write(content)
