import type { VercelRequest, VercelResponse } from '@vercel/node';
import { createClient } from '@sanity/client';

const client = createClient({
  projectId: process.env.VITE_SANITY_PROJECT_ID || process.env.SANITY_PROJECT_ID,
  dataset: process.env.VITE_SANITY_DATASET || process.env.SANITY_DATASET || 'production',
  token: process.env.VITE_SANITY_API_TOKEN || process.env.SANITY_API_TOKEN,
  useCdn: false,
  apiVersion: '2023-01-01',
});

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { email, password } = req.body;

    const user = await client.fetch(
      `*[_type == "user" && email == $email][0]`,
      { email }
    );

    if (!user || user.password !== password) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    return res.status(200).json({ success: true, user });
  } catch (error: any) {
    return res.status(500).json({ error: error.message || 'Server error' });
  }
}
