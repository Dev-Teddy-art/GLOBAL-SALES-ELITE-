import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add sanityClient import
if 'import { sanityClient }' not in content:
    content = content.replace("import { motion, AnimatePresence } from 'motion/react';", "import { motion, AnimatePresence } from 'motion/react';\nimport { sanityClient } from './lib/sanity';")

# Add state to LandingPage
state_add = """  const [networkSize, setNetworkSize] = React.useState<number | null>(null);
  
  React.useEffect(() => {
    sanityClient.fetch('count(*[_type == "user"])').then(count => {
      setNetworkSize(count);
    }).catch(console.error);
  }, []);"""

content = content.replace('const [errorMsg, setErrorMsg] = React.useState(\'\');', 'const [errorMsg, setErrorMsg] = React.useState(\'\');\n' + state_add)

# Replace mock data
content = content.replace('<div className="text-blue-400 font-mono font-bold">₦12.5M</div>', '<div className="text-blue-400 font-mono font-bold">Dynamic</div>')
content = content.replace('<div className="text-blue-400 font-mono font-bold">1,402</div>', '<div className="text-blue-400 font-mono font-bold">{networkSize !== null ? networkSize : "..."}</div>')

with open('src/App.tsx', 'w') as f:
    f.write(content)
