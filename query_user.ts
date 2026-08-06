import { sanityClient } from './src/lib/sanity.js';

async function run() {
  const users = await sanityClient.fetch(`*[_type == "user"] | order(createdAt desc)[0...5]`);
  console.log(users.map((u: any) => ({ email: u.email, name: u.displayName, createdAt: u.createdAt, role: u.role, referralCode: u.referralCode })));
}

run().catch(console.error);
