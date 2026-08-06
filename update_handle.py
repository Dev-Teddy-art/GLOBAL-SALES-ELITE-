import re

with open('src/contexts/AuthContext.tsx', 'r') as f:
    content = f.read()

old_handle = '''const handleSanityError = (err: any) => {
  if (err.message && (err.message.includes('Project ID') || err.message.includes('API Token') || err.message.includes('URL') || err.message.includes('project ID'))) {
    throw new Error("Missing Sanity Project ID or API Token. Please check your environment variables.");
  }
  // Generic fallback if it's a fetch or connection error from sanity
  if (err.name === 'TypeError' && err.message.includes('fetch')) {
    throw new Error("Missing Sanity Project ID or API Token. Please check your environment variables.");
  }
  if (err.response && (err.response.statusCode === 401 || err.response.statusCode === 403 || err.response.statusCode === 404)) {
    throw new Error("Missing Sanity Project ID or API Token. Please check your environment variables.");
  }
  throw err;
};'''

new_handle = '''const handleSanityError = (err: any) => {
  if (err.message && (err.message.includes('Project ID') || err.message.includes('API Token') || err.message.includes('URL') || err.message.includes('project ID') || err.message.includes('dataset'))) {
    throw new Error("Missing Sanity Project ID or API Token. Please check your environment variables.");
  }
  if (err.name === 'TypeError' && err.message.includes('fetch')) {
    throw new Error("Network error connecting to the database. Please check your connection.");
  }
  if (err.response && (err.response.statusCode === 401 || err.response.statusCode === 403 || err.response.statusCode === 404)) {
    throw new Error("Missing Sanity Project ID or API Token. Please check your environment variables.");
  }
  // Generic fallback for any other unformatted API error
  throw new Error(err.message ? `Database connection failed. Please try again later.` : "An unexpected error occurred.");
};'''

content = content.replace(old_handle, new_handle)

with open('src/contexts/AuthContext.tsx', 'w') as f:
    f.write(content)
