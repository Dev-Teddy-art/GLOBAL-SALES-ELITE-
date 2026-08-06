const { createClient } = require('@sanity/client');
const client = createClient({ 
  projectId: 'test', 
  dataset: 'test', 
  useCdn: false, 
  apiVersion: '2023-05-03',
  fetch: async (url, init) => {
    console.log("CUSTOM FETCH CALLED WITH URL:", url);
    return { ok: true, json: async () => ({ result: "mock" }) };
  }
});
client.fetch('*').then(console.log).catch(console.error);
