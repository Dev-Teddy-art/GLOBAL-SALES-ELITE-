import re

# Update UserProfile interface
with open('src/contexts/AuthContext.tsx', 'r') as f:
    content = f.read()

profile_def = """  profileImage?: string;
  avatarUrl?: string;"""

new_profile_def = """  profileImage?: string;
  avatarUrl?: string;
  notifications?: { id: string; message: string; read: boolean; createdAt: string; }[];"""
content = content.replace(profile_def, new_profile_def)

with open('src/contexts/AuthContext.tsx', 'w') as f:
    f.write(content)

# Update server.ts
with open('server.ts', 'r') as f:
    server_content = f.read()

import_replacement = """      const createdDoc = await sanityClient.create(newUserDoc);"""
new_import_replacement = """      const createdDoc = await sanityClient.create(newUserDoc);
      
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
"""

server_content = server_content.replace(import_replacement, new_import_replacement)

# Mark notification as read endpoint
mark_read_endpoint = """
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
"""
server_content = server_content.replace("app.post('/api/auth/signup',", mark_read_endpoint + "\n  app.post('/api/auth/signup',")

with open('server.ts', 'w') as f:
    f.write(server_content)
