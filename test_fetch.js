const { createClient } = require('@sanity/client');
console.log(createClient({ projectId: 'test', dataset: 'test', fetch: () => {} }));
