import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Replace AdminTreeNode definition
content = content.replace("function AdminTreeNode({ node, level }: { node: any, level: number }) {", "const AdminTreeNode: React.FC<{ node: any, level: number }> = ({ node, level }) => {")

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
