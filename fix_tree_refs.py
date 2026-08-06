import re

with open('src/components/ReferralTree.tsx', 'r') as f:
    content = f.read()

old_init = '''    // Initialize all nodes
    users.forEach(u => {
      nodeMap.set(u.id, { ...u, children: [], depth: 0 });
      nodeMap.set(u.referralCode, { ...u, children: [], depth: 0 }); // Support lookup by ref code too
    });'''

new_init = '''    // Initialize all nodes
    users.forEach(u => {
      const node = { ...u, children: [], depth: 0 };
      nodeMap.set(u.id, node);
      if (u.referralCode) {
        nodeMap.set(u.referralCode, node); // Support lookup by ref code too, pointing to same reference
      }
    });'''

content = content.replace(old_init, new_init)

with open('src/components/ReferralTree.tsx', 'w') as f:
    f.write(content)
