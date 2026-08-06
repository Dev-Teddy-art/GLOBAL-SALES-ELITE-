import re

with open('server.ts', 'r') as f:
    content = f.read()

reset_endpoint = """
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
"""

content = content.replace("  app.post('/api/sanity/query',", reset_endpoint + "\n  app.post('/api/sanity/query',")

with open('server.ts', 'w') as f:
    f.write(content)

