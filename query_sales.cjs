const { createClient } = require('@sanity/client');

const sanityClient = createClient({
  projectId: 'iyon82wq',
  dataset: 'production',
  token: 'sk62sHenAVVHGWOO40MsYS3cw1F3NhCNQQJ8ZTtrpa8Y61QjPyqFEx1PbUYcHlo20Si1rPEYpJE7kAUlfgZvxGVZ3QTBkGuepyNYDLq0mAPXxC6zx4bmPdKDCwyr0nYmt8IZd47PMDef7bfuSE4uwHiy45gBXE2vooitQBEKSJZdw9TCIxyh',
  apiVersion: '2023-05-03',
  useCdn: false,
});

async function run() {
  const sales = await sanityClient.fetch(`*[_type == "sale"]{_id, userId, propertyName, amount, status}`);
  console.log(sales);
}
run().catch(console.error);
