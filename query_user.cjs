const { createClient } = require('@sanity/client');
require('dotenv').config();

const sanityClient = createClient({
  projectId: process.env.SANITY_PROJECT_ID,
  dataset: process.env.SANITY_DATASET,
  useCdn: false,
  apiVersion: '2023-10-01',
  token: process.env.SANITY_API_TOKEN
});

async function run() {
  const users = await sanityClient.fetch(`*[_type == "user" && (displayName match "GLOBAL SALES" || firstName match "GLOBAL")]`);
  console.log(users.map(u => ({ email: u.email, name: u.displayName, createdAt: u.createdAt, role: u.role, referralCode: u.referralCode })));
}

run().catch(console.error);
