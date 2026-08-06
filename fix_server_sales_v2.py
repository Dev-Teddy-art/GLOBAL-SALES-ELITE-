import re

with open('server.ts', 'r') as f:
    content = f.read()

old_sales = """  app.post('/api/sales', async (req, res) => {
    try {
      const { userId, amount } = req.body;
      const user = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: userId });
      if (!user) return res.status(404).json({ error: "User not found" });
      
      const sale = await sanityClient.create({
        _type: 'sale',
        userId: user._id,
        userRef: { _type: 'reference', _ref: user._id },
        amount: amount,
        status: 'pending',
        createdAt: new Date().toISOString()
      });
      res.json({ success: true, sale });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.get('/api/admin/sales', async (req, res) => {
    try {
      const adminId = req.query.adminId;
      const admin = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: adminId });
      if (!admin || (admin.role !== 'admin' && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      const sales = await sanityClient.fetch(`*[_type == "sale" && status == "pending"] | order(createdAt asc) {
        ...,
        userRef->{displayName, email, bankName, bankAccountNumber, bankAccountName}
      }`);
      res.json(withdrawals);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });"""

new_sales = """  app.post('/api/sales', async (req, res) => {
    try {
      const { userId, amount, propertyName, dateSold } = req.body;
      const user = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: userId });
      if (!user) return res.status(404).json({ error: "User not found" });
      
      const sale = await sanityClient.create({
        _type: 'sale',
        userId: user._id,
        userRef: { _type: 'reference', _ref: user._id },
        amount: amount,
        propertyName: propertyName,
        dateSold: dateSold,
        status: 'pending',
        createdAt: new Date().toISOString()
      });
      res.json({ success: true, sale });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.get('/api/admin/sales', async (req, res) => {
    try {
      const adminId = req.query.adminId;
      const admin = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: adminId });
      if (!admin || (admin.role !== 'admin' && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      const sales = await sanityClient.fetch(`*[_type == "sale"] | order(createdAt desc) {
        ...,
        userRef->{displayName, email, bankName, bankAccountNumber, bankAccountName}
      }`);
      res.json(sales);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });"""

content = content.replace(old_sales, new_sales)

with open('server.ts', 'w') as f:
    f.write(content)
