const fs = require('fs');
let code = fs.readFileSync('server.ts', 'utf8');

const targetEndpoint = `  app.post('/api/admin/sales/payout', async (req, res) => {
    try {
      const { adminId, saleId, payoutStatus } = req.body;
      const admin = await sanityClient.fetch(\`*[_type == "user" && _id == $id][0]\`, { id: adminId });
      if (!admin || (admin.role !== 'admin' && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      const updated = await sanityClient.patch(saleId).set({ payoutStatus }).commit();
      res.json({ success: true, sale: updated });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });`;

const newEndpoint = `  app.post('/api/admin/sales/payout', async (req, res) => {
    try {
      const { adminId, saleId, payoutStatus } = req.body;
      const admin = await sanityClient.fetch(\`*[_type == "user" && _id == $id][0]\`, { id: adminId });
      if (!admin || (admin.role !== 'admin' && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      const updated = await sanityClient.patch(saleId).set({ payoutStatus }).commit();
      
      if (payoutStatus === 'paid') {
        try {
          const saleWithUser = await sanityClient.fetch(\`*[_type == "sale" && _id == $id][0] {
            ...,
            userRef->{email, displayName, firstName}
          }\`, { id: saleId });
          
          if (saleWithUser?.userRef?.email) {
            const userEmail = saleWithUser.userRef.email;
            const userName = saleWithUser.userRef.firstName || saleWithUser.userRef.displayName || 'Realtor';
            
            if (process.env.RESEND_API_KEY) {
              const resend = new Resend(process.env.RESEND_API_KEY);
              await resend.emails.send({
                from: 'Global Sales Elite <noreply@globalsaleselite.com>',
                to: [userEmail],
                subject: 'Commission Payout Confirmed! 🎉',
                html: \`<p>Hi \${userName},</p><p>Great news! Your commission payout of ₦\${(saleWithUser.amount || 0).toLocaleString()} for the sale of <strong>\${saleWithUser.propertyName || 'Property'}</strong> has been processed and paid.</p><p>Keep up the great work!</p><p>Best,<br/>Global Sales Elite Admin Team</p>\`
              });
              console.log(\`[Email] Payout confirmation email sent to \${userEmail}\`);
            } else {
              console.log(\`[Mock Email] Would send payout confirmation email to \${userEmail} for sale \${saleId}\`);
            }
          }
        } catch (emailErr) {
          console.error("Failed to send payout confirmation email:", emailErr);
        }
      }

      res.json({ success: true, sale: updated });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });`;

code = code.replace(targetEndpoint, newEndpoint);
fs.writeFileSync('server.ts', code);
