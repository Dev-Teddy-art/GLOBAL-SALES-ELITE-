const { createClient } = require('@sanity/client');
console.log(Object.keys(createClient({ projectId: 'test', dataset: 'test' })));
