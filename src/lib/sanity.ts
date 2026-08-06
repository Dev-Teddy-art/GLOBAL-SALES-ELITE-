// Proxy client for browser usage to bypass CORS
export const sanityClient = {
  fetch: async (query: string, params?: any) => {
    const res = await fetch('/api/sanity/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, params })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to query database');
    return data;
  }
};
