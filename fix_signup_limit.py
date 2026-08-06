import re

with open('server.ts', 'r') as f:
    content = f.read()

old_block = '''      if (finalSponsorId !== 'admin') {
        const parentUser = await sanityClient.fetch(`*[_type == "user" && referralCode == $code][0]`, { code: finalSponsorId });
        if (parentUser) {
          parentRgt = parentUser.rgt || 0;
        } else {
          const parentById = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: finalSponsorId });
          if (parentById) {
            parentRgt = parentById.rgt || 0;
          } else {
            const maxRgtUser = await sanityClient.fetch(`*[_type == "user"] | order(rgt desc)[0]`);
            if (maxRgtUser) {
              parentRgt = (maxRgtUser.rgt || 0) + 1;
            }
          }
        }
      } else {'''

new_block = '''      if (finalSponsorId !== 'admin') {
        let parentUser = await sanityClient.fetch(`*[_type == "user" && referralCode == $code][0]`, { code: finalSponsorId });
        if (!parentUser) {
          parentUser = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: finalSponsorId });
        }
        
        if (parentUser) {
          if (parentUser.role !== 'admin' && !parentUser.isAdmin) {
            const directChildrenCount = await sanityClient.fetch(`count(*[_type == "user" && sponsorId in [$refCode, $id]])`, { refCode: parentUser.referralCode, id: parentUser._id });
            if (directChildrenCount >= 2) {
              return res.status(400).json({ error: "This sponsor has reached their maximum limit of 2 direct referrals." });
            }
          }
          parentRgt = parentUser.rgt || 0;
        } else {
          const maxRgtUser = await sanityClient.fetch(`*[_type == "user"] | order(rgt desc)[0]`);
          if (maxRgtUser) {
            parentRgt = (maxRgtUser.rgt || 0) + 1;
          }
        }
      } else {'''

if old_block in content:
    content = content.replace(old_block, new_block)
else:
    print("Could not find old block")

with open('server.ts', 'w') as f:
    f.write(content)
