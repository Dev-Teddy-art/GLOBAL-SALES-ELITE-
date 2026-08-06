import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

if "import { ReferralTree }" not in content:
    content = content.replace("import { motion } from 'motion/react';", "import { motion } from 'motion/react';\nimport { ReferralTree } from './ReferralTree';")

old_network_view = '''          {profile.isAdmin || profile.role === 'admin' ? (
            <div className="text-gray-500 py-8 text-center bg-gray-50 rounded-xl border border-gray-100">
              <Network className="mx-auto h-8 w-8 mb-2 text-gray-400" />
              <p>Network Tree is managed in the Admin Console.</p>
              <button onClick={() => navigate('/admin')} className="mt-4 text-[#e03126] font-medium hover:underline">Go to Admin Console</button>
            </div>
          ) : ('''

new_network_view = '''          {profile.isAdmin || profile.role === 'admin' ? (
            <ReferralTree users={allUsers} isAdminView={true} />
          ) : (
            <ReferralTree users={allUsers} rootUserId={profile.id || profile._id} isAdminView={false} />
          )}
          {false ? ('''

content = content.replace(old_network_view, new_network_view)

# Delete the old flat list logic. It's wrapped in {false ? ( ... )} so we can just let it sit or remove it.
# The user doesn't need to see the flat downline list if we use the ReferralTree.
# But `allUsers` should be populated for standard users too.
# Let's check `fetchData` in Dashboard.tsx
with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
