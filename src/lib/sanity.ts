import { createClient } from '@sanity/client';

export const sanityClient = createClient({
  projectId: import.meta.env.VITE_SANITY_PROJECT_ID || 'your_project_id',
  dataset: import.meta.env.VITE_SANITY_DATASET || 'production',
  token: import.meta.env.VITE_SANITY_API_TOKEN,
  useCdn: false,
  apiVersion: '2023-01-01',
});

export async function sanityQuery(query: string, params: Record<string, any> = {}) {
  return await sanityClient.fetch(query, params);
}
