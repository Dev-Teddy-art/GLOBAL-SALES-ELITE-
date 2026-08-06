const { createClient } = require('@sanity/client');
const client = createClient({ 
  projectId: 'test', 
  dataset: 'test', 
  useCdn: false, 
  apiVersion: '2023-05-03',
  apiHost: 'http://localhost:3000'
});
console.log(client.getUrl('/data/query/test?query=*'));
