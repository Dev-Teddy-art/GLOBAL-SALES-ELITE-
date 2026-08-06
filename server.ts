import 'dotenv/config';
import express from 'express';
import path from 'path';
import { createServer as createViteServer } from 'vite';
import { createClient } from '@sanity/client';
import bcrypt from 'bcryptjs';
import { sendPayoutConfirmationEmail } from './src/lib/email';

const sanityClient = createClient({
  projectId: 'iyon82wq',
  dataset: 'production',
  token: 'sk62sHenAVVHGWOO40MsYS3cw1F3NhCNQQJ8ZTtrpa8Y61QjPyqFEx1PbUYcHlo20Si1rPEYpJE7kAUlfgZvxGVZ3QTBkGuepyNYDLq0mAPXxC6zx4bmPdKDCwyr0nYmt8IZd47PMDef7bfuSE4uwHiy45gBXE2vooitQBEKSJZdw9TCIxyh',
  apiVersion: '2023-05-03',
  useCdn: false,
  ignoreBrowserTokenWarning: true
});

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json({ limit: '10mb' }));

  app.get('/api/auth/me', async (req, res) => {
    try {
      const { id } = req.query;
      const userDoc = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id });
      res.json({ user: userDoc });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/api/auth/login', async (req, res) => {
    try {
      const { email, password } = req.body;
      const userDoc = await sanityClient.fetch(`*[_type == "user" && email == $email][0]`, { email });
      
      if (!userDoc) {
        return res.status(400).json({ error: "Account not found. Please sign up first." });
      }
      
      const isValid = bcrypt.compareSync(password, userDoc.passwordHash || '');
      if (!isValid) {
        return res.status(400).json({ error: "Invalid email or password." });
      }
      
      await sanityClient.patch(userDoc._id).set({ lastLoginAt: new Date().toISOString() }).commit();
      res.json({ user: userDoc });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  
  app.post('/api/auth/notifications/read', async (req, res) => {
    try {
      const { userId } = req.body;
      const user = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: userId });
      if (user && user.notifications) {
        const updatedNotifications = user.notifications.map((n: any) => ({ ...n, read: true }));
        await sanityClient.patch(userId).set({ notifications: updatedNotifications }).commit();
        res.json({ success: true });
      } else {
        res.json({ success: true });
      }
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/api/auth/signup', async (req, res) => {
    try {
      const { password, extraData } = req.body;
      
      const existing = await sanityClient.fetch(`*[_type == "user" && email == $email][0]`, { email: extraData.email });
      if (existing) {
        return res.status(400).json({ error: "An account with this email already exists. Please log in." });
      }
      
      const salt = bcrypt.genSaltSync(10);
      const passwordHash = bcrypt.hashSync(password, salt);
      
      let finalRole = 'user';
      let finalSponsorId = extraData.sponsorId || 'admin';
      if (extraData.email === 'info@globalsaleselite.com') {
        finalRole = 'admin';
        finalSponsorId = 'admin';
      }
      
      let parentRgt = 0;
      let newLft = 1;
      let newRgt = 2;
      
      if (finalSponsorId !== 'admin') {
        let parentUser = await sanityClient.fetch(`*[_type == "user" && referralCode == $code][0]`, { code: finalSponsorId });
        if (!parentUser) {
          parentUser = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: finalSponsorId });
        }
        
        if (parentUser) {
          if (parentUser.role !== 'admin' && !parentUser.isAdmin) {
            const directChildrenCount = await sanityClient.fetch(`count(*[_type == "user" && sponsorId in [$refCode, $id]])`, { refCode: parentUser.referralCode, id: parentUser._id });
            if (directChildrenCount >= 2) {
              return res.status(400).json({ error: "This sponsor has reached their maximum limit of 2 direct referrals." });
            }
          }
          parentRgt = parentUser.rgt || 0;
        } else {
          const maxRgtUser = await sanityClient.fetch(`*[_type == "user"] | order(rgt desc)[0]`);
          if (maxRgtUser) {
            parentRgt = (maxRgtUser.rgt || 0) + 1;
          }
        }
      } else {
        const maxRgtUser = await sanityClient.fetch(`*[_type == "user"] | order(rgt desc)[0]`);
        if (maxRgtUser) {
          parentRgt = (maxRgtUser.rgt || 0) + 1;
        }
      }
      
      if (parentRgt > 0) {
        newLft = parentRgt;
        newRgt = parentRgt + 1;
        
        const shiftLftQuery = await sanityClient.fetch(`*[_type == "user" && lft > $rgt]`, { rgt: parentRgt });
        const shiftRgtQuery = await sanityClient.fetch(`*[_type == "user" && rgt >= $rgt]`, { rgt: parentRgt });
        
        const transaction = sanityClient.transaction();
        shiftLftQuery.forEach((doc: any) => {
           transaction.patch(doc._id, p => p.inc({ lft: 2 }));
        });
        shiftRgtQuery.forEach((doc: any) => {
           transaction.patch(doc._id, p => p.inc({ rgt: 2 }));
        });
        await transaction.commit();
      }
      
      const newUserDoc = {
        _type: 'user',
        email: extraData.email,
        passwordHash,
        displayName: `${extraData.firstName || ''} ${extraData.lastName || ''}`.trim() || '',
        role: finalRole,
        isAdmin: finalRole === 'admin',
        sponsorId: finalSponsorId,
        referralCode: Math.random().toString(36).substring(2, 8).toUpperCase(),
        createdAt: new Date().toISOString(),
        lastLoginAt: new Date().toISOString(),
        lft: newLft,
        rgt: newRgt,
        firstName: extraData.firstName || '',
        lastName: extraData.lastName || '',
        address: extraData.address || '',
        bankAccountNumber: extraData.bankAccountNumber || '',
        bankAccountName: extraData.bankAccountName || '',
        bankName: extraData.bankName || '',
        avatarUrl: extraData.avatarUrl || '',
      };
      
      const createdDoc = await sanityClient.create(newUserDoc);
      
      if (finalSponsorId !== 'admin') {
        let pUser = await sanityClient.fetch(`*[_type == "user" && referralCode == $code][0]`, { code: finalSponsorId });
        if (!pUser) {
          pUser = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: finalSponsorId });
        }
        if (pUser) {
          await sanityClient.patch(pUser._id)
            .setIfMissing({ notifications: [] })
            .insert('after', 'notifications[-1]', [{
               id: Math.random().toString(36).substring(2, 10),
               message: `🎉 Someone joined using your referral link!`,
               read: false,
               createdAt: new Date().toISOString()
            }])
            .commit();
        }
      }

      res.json({ user: createdDoc });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });



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
        .unset(['avatarUrl'])
        .commit();
        
      res.json({ url: asset.url, user: updatedUser });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });


  app.post("/api/auth/update-settings", async (req, res) => {
    try {
      const { userId, avatarUrl, newPassword, bankName, bankAccountNumber, bankAccountName } = req.body;
      const updates: any = {};
      if (avatarUrl !== undefined) updates.avatarUrl = avatarUrl;
      if (bankName !== undefined) updates.bankName = bankName;
      if (bankAccountNumber !== undefined) updates.bankAccountNumber = bankAccountNumber;
      if (bankAccountName !== undefined) updates.bankAccountName = bankAccountName;
      if (newPassword) {
        const salt = bcrypt.genSaltSync(10);
        updates.passwordHash = bcrypt.hashSync(newPassword, salt);
      }
      if (Object.keys(updates).length > 0) {
        const updatedUser = await sanityClient.patch(userId).set(updates).commit();
        res.json({ user: updatedUser });
      } else {
        res.json({ success: true });
      }
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/api/auth/update-avatar', async (req, res) => {
    try {
      const { userId, avatarUrl } = req.body;
      const updatedUser = await sanityClient.patch(userId)
        .set({ avatarUrl })
        .unset(['profileImage'])
        .commit();
      res.json({ user: updatedUser });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });


  app.post('/api/auth/reset-password', async (req, res) => {
    try {
      const { email, newPassword } = req.body;
      const user = await sanityClient.fetch(`*[_type == "user" && email == $email][0]`, { email });
      if (!user) {
        return res.status(404).json({ error: "User not found." });
      }

      const salt = bcrypt.genSaltSync(10);
      const passwordHash = bcrypt.hashSync(newPassword, salt);

      await sanityClient.patch(user._id)
        .set({ passwordHash })
        .commit();

      res.json({ success: true });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/api/sanity/query', async (req, res) => {
    try {
      const { query, params } = req.body;
      const data = await sanityClient.fetch(query, params);
      res.json(data);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });




  app.post('/api/sales', async (req, res) => {
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
  });

  app.post("/api/admin/sales/delete", async (req, res) => {
    try {
      const { adminId, saleId } = req.body;
      const admin = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: adminId });
      if (!admin || (admin.role !== "admin" && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      await sanityClient.delete(saleId);
      res.json({ success: true });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/api/admin/sales/process', async (req, res) => {
    try {
      const { adminId, saleId, status } = req.body; // status: 'approved' | 'rejected'
      const admin = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: adminId });
      if (!admin || (admin.role !== 'admin' && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      const updated = await sanityClient.patch(saleId).set({ status }).commit();
      res.json({ success: true, sale: updated });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/api/admin/sales/payout', async (req, res) => {
    try {
      const { adminId, saleId, payoutStatus } = req.body;
      const admin = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: adminId });
      if (!admin || (admin.role !== 'admin' && !admin.isAdmin)) {
        return res.status(403).json({ error: "Unauthorized" });
      }
      const updated = await sanityClient.patch(saleId).set({ payoutStatus }).commit();
      
      if (payoutStatus === 'paid' || payoutStatus === 'Paid' || payoutStatus?.toLowerCase() === 'paid') {
        try {
          const saleWithUser = await sanityClient.fetch(`*[_type == "sale" && _id == $id][0] {
            ...,
            userRef->{email, displayName, firstName}
          }`, { id: saleId });
          
          if (saleWithUser?.userRef?.email) {
            const userEmail = saleWithUser.userRef.email;
            const userName = saleWithUser.userRef.firstName || saleWithUser.userRef.displayName || 'Realtor';
            const amount = saleWithUser.amount || 0;
            const propertyName = saleWithUser.propertyName || 'Property';
            
            await sendPayoutConfirmationEmail(userEmail, userName, amount, propertyName);
          }
        } catch (emailErr) {
          console.error("Failed to send payout confirmation email:", emailErr);
        }
      }

      res.json({ success: true, sale: updated });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

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

  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on port ${PORT}`);
  });
}

startServer();
