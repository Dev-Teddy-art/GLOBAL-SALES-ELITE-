import { createClient } from '@sanity/client';

const projectId = 
  (typeof process !== 'undefined' && process.env.NEXT_PUBLIC_SANITY_PROJECT_ID) || 
  (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_SANITY_PROJECT_ID);

const dataset = 
  (typeof process !== 'undefined' && process.env.NEXT_PUBLIC_SANITY_DATASET) || 
  (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_SANITY_DATASET) || 
  'production';

const token = 
  (typeof process !== 'undefined' && process.env.SANITY_API_TOKEN) || 
  (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_SANITY_API_TOKEN);

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
