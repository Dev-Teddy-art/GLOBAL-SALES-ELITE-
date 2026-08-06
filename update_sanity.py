import os

with open('src/lib/sanity.ts', 'w') as f:
    f.write("""import { createClient } from '@sanity/client';

const projectId = import.meta.env.VITE_NEXT_PUBLIC_SANITY_PROJECT_ID || import.meta.env.VITE_SANITY_PROJECT_ID;
const dataset = import.meta.env.VITE_NEXT_PUBLIC_SANITY_DATASET || import.meta.env.VITE_SANITY_DATASET || 'production';
const token = import.meta.env.VITE_SANITY_API_TOKEN || import.meta.env.VITE_SANITY_TOKEN;

const dummyClient = {
  fetch: async () => { throw new Error("Missing Sanity Project ID or API Token. Please check your environment variables."); },
  create: async () => { throw new Error("Missing Sanity Project ID or API Token. Please check your environment variables."); },
  patch: () => ({ set: () => ({ commit: async () => { throw new Error("Missing Sanity Project ID or API Token. Please check your environment variables."); } }) }),
  transaction: () => ({ patch: () => {}, commit: async () => { throw new Error("Missing Sanity Project ID or API Token. Please check your environment variables."); } })
} as any;

export const sanityClient = projectId ? createClient({
  projectId,
  dataset,
  useCdn: false,
  apiVersion: '2023-05-03',
  token
}) : dummyClient;
""")
