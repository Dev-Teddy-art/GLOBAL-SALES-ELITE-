const { createClient } = require('@sanity/client');

const sanityClient = createClient({
  projectId: 'iyon82wq',
  dataset: 'production',
  token: 'sk62sHenAVVHGWOO40MsYS3cw1F3NhCNQQJ8ZTtrpa8Y61QjPyqFEx1PbUYcHlo20Si1rPEYpJE7kAUlfgZvxGVZ3QTBkGuepyNYDLq0mAPXxC6zx4bmPdKDCwyr0nYmt8IZd47PMDef7bfuSE4uwHiy45gBXE2vooitQBEKSJZdw9TCIxyh',
  apiVersion: '2023-05-03',
  useCdn: false,
});

async function run() {
  const transaction = sanityClient.transaction();

  // Promote info@globalsaleselite.com
  transaction.patch('QMB6N1bjfvfdxsfnPu1nCL', p => p.set({ role: 'admin', isAdmin: true, sponsorId: 'admin', lft: 2, rgt: 3 })); // I might need to run nested sets fix after. Let's just set the role for now.
  
  // Demote mypropteeapp@gmail.com
  transaction.patch('gz9dTbVKIQuQwPPp9C6Bir', p => p.set({ role: 'user', isAdmin: false }));

  await transaction.commit();
  console.log("Success!");
}
run().catch(console.error);
