import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Make sure standard users also set allUsers including themselves
old_fetch = '''        if (profile.isAdmin || profile.role === 'admin') {
          const users = await sanityClient.fetch(`*[_type == "user"]`);
          setAllUsers(users.map((u: any) => ({ ...u, id: u._id })));
        } else {
          // Fetch downline using Nested Set Model bounds
          const allDescendantsRaw = await sanityClient.fetch(`*[_type == "user" && lft > $lft && rgt < $rgt]`, { lft: profile.lft, rgt: profile.rgt });
          const allDescendants = allDescendantsRaw.map((u: any) => ({ ...u, id: u._id }));'''

new_fetch = '''        if (profile.isAdmin || profile.role === 'admin') {
          const users = await sanityClient.fetch(`*[_type == "user"]`);
          setAllUsers(users.map((u: any) => ({ ...u, id: u._id })));
        } else {
          // Fetch downline using Nested Set Model bounds
          const allDescendantsRaw = await sanityClient.fetch(`*[_type == "user" && lft > $lft && rgt < $rgt]`, { lft: profile.lft, rgt: profile.rgt });
          const allDescendants = allDescendantsRaw.map((u: any) => ({ ...u, id: u._id }));
          
          // For the ReferralTree, we need to provide the user themselves as the root
          setAllUsers([{ ...profile, id: profile._id || profile.id || '' }, ...allDescendants]);'''

content = content.replace(old_fetch, new_fetch)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
