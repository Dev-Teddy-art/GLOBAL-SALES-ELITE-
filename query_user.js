const { createClient } = require('@sanity/client');
const fs = require('fs');
require('dotenv').config();

const sanityClient = createClient({
  projectId: process.env.SANITY_PROJECT_ID,
  dataset: process.env.SANITY_DATASET,
  useCdn: false,
  apiVersion: '2023-10-01',
  token: process.env.SANITY_API_TOKEN
});

async function run() {
  const users = await sanityClient.fetch(`*[_type == "user" && displayName match "Global Sales" || firstName match "Global"]`);
  console.log(users);
}

run().catch(console.error);
