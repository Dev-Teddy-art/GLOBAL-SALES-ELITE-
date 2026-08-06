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
  try {
    const query = req.method === 'POST' ? req.body.query : req.query.query;
    const params = req.method === 'POST' ? req.body.params : {};

    if (!query) {
      return res.status(400).json({ error: 'Query parameter is required' });
    }

    const data = await client.fetch(query, params);
    return res.status(200).json(data);
  } catch (error: any) {
    return res.status(500).json({ error: error.message || 'Query execution error' });
  }
}
