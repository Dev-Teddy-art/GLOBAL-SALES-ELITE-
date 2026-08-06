import re

# 1. Update server.ts
with open('server.ts', 'r') as f:
    server_content = f.read()

withdrawal_endpoints = """
  app.post('/api/withdrawals', async (req, res) => {
    try {
      const { userId, amount } = req.body;
      const user = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: userId });
      if (!user) return res.status(404).json({ error: "User not found" });
      
      const withdrawal = await sanityClient.create({
        _type: 'withdrawal',
        userId: user._id,
        userRef: { _type: 'reference', _ref: user._id },
        amount: amount,
        status: 'pending',
        createdAt: new Date().toISOString()
      });
      res.json({ success: true, withdrawal });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.get('/api/admin/withdrawals', async (req, res) => {
    try {
      const adminId = req.query.adminId;
      const admin = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: adminId });
      if (!admin || (admin.role !== 'admin' && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      const withdrawals = await sanityClient.fetch(`*[_type == "withdrawal" && status == "pending"] | order(createdAt asc) {
        ...,
        userRef->{displayName, email, bankName, bankAccountNumber, bankAccountName}
      }`);
      res.json(withdrawals);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/api/admin/withdrawals/process', async (req, res) => {
    try {
      const { adminId, withdrawalId, status } = req.body; // status: 'approved' | 'rejected'
      const admin = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: adminId });
      if (!admin || (admin.role !== 'admin' && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      const updated = await sanityClient.patch(withdrawalId).set({ status }).commit();
      res.json({ success: true, withdrawal: updated });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });
"""
server_content = server_content.replace("  app.post('/api/admin/update-user',", withdrawal_endpoints + "\n  app.post('/api/admin/update-user',")
with open('server.ts', 'w') as f:
    f.write(server_content)
