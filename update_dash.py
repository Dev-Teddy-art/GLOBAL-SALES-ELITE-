import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

old_fetchData = '''    const fetchData = async () => {
      if (!user || !profile) return;
      
      try {
        if (profile.isAdmin || profile.role === 'admin') {
          const users = await sanityClient.fetch(`*[_type == "user"]`);
          setAllUsers(users.map((u: any) => ({ ...u, id: u._id })));
        } else {
          // Fetch downline using Nested Set Model bounds
          const allDescendantsRaw = await sanityClient.fetch(`*[_type == "user" && lft > $lft && rgt < $rgt]`, { lft: profile.lft, rgt: profile.rgt });
          const allDescendants = allDescendantsRaw.map((u: any) => ({ ...u, id: u._id }));

          // We can group them by level in memory by building a quick lookup
          const idToNode = new Map<string, any>();
          idToNode.set(profile.referralCode, { ...profile, __level: 0 });
          idToNode.set(profile._id, { ...profile, __level: 0 }); // fallback for sponsorId as UID
          
          allDescendants.forEach((u: any) => {
              idToNode.set(u.referralCode, { ...u, __level: -1 });
              idToNode.set(u.id, { ...u, __level: -1 });
          });

          // Calculate levels
          let changed = true;
          while (changed) {
              changed = false;
              allDescendants.forEach((u: any) => {
                  const node = idToNode.get(u.id);
                  if (node.__level === -1) {
                      const parent = idToNode.get(u.sponsorId);
                      if (parent && parent.__level >= 0) {
                          node.__level = parent.__level + 1;
                          idToNode.set(u.referralCode, node);
                          idToNode.set(u.id, node);
                          changed = true;
                      }
                  }
              });
          }

          const l1Users = allDescendants.filter((u: any) => idToNode.get(u.id).__level === 1);
          const l2Users = allDescendants.filter((u: any) => idToNode.get(u.id).__level === 2);
          const l3Users = allDescendants.filter((u: any) => idToNode.get(u.id).__level === 3);
          
          setDownline(l1Users);
          setLevel2Downline(l2Users);
          setLevel3Downline(l3Users);

          // Fetch sponsor name
          if (profile.sponsorId && profile.sponsorId !== 'admin') {
            const sponsorDoc = await sanityClient.fetch(`*[_type == "user" && (referralCode == $sid || _id == $sid)][0]`, { sid: profile.sponsorId });
            if (sponsorDoc) {
              setSponsorName(sponsorDoc.displayName || 'Unknown');
            }
          }
        }
      } catch (err) {
        console.error("Error fetching data:", err);
      } finally {
        setLoading(false);
      }
    };'''

new_fetchData = '''    const fetchData = async () => {
      if (!user || !profile) return;
      
      try {
        if (profile.isAdmin || profile.role === 'admin') {
          const users = await sanityClient.fetch(`*[_type == "user"]`);
          setAllUsers(users.map((u: any) => ({ ...u, id: u._id })));
        } else {
          // Fetch downline using Nested Set Model bounds
          const allDescendantsRaw = await sanityClient.fetch(`*[_type == "user" && lft > $lft && rgt < $rgt]`, { lft: profile.lft, rgt: profile.rgt });
          const allDescendants = allDescendantsRaw.map((u: any) => ({ ...u, id: u._id }));

          // We can group them by level in memory by building a quick lookup
          const idToNode = new Map<string, any>();
          idToNode.set(profile.referralCode, { ...profile, __level: 0 });
          idToNode.set(profile._id, { ...profile, __level: 0 }); // fallback for sponsorId as UID
          
          allDescendants.forEach((u: any) => {
              idToNode.set(u.referralCode, { ...u, __level: -1 });
              idToNode.set(u.id, { ...u, __level: -1 });
          });

          // Calculate levels
          let changed = true;
          while (changed) {
              changed = false;
              allDescendants.forEach((u: any) => {
                  const node = idToNode.get(u.id);
                  if (node.__level === -1) {
                      const parent = idToNode.get(u.sponsorId);
                      if (parent && parent.__level >= 0) {
                          node.__level = parent.__level + 1;
                          idToNode.set(u.referralCode, node);
                          idToNode.set(u.id, node);
                          changed = true;
                      }
                  }
              });
          }

          const l1Users = allDescendants.filter((u: any) => idToNode.get(u.id).__level === 1);
          const l2Users = allDescendants.filter((u: any) => idToNode.get(u.id).__level === 2);
          const l3Users = allDescendants.filter((u: any) => idToNode.get(u.id).__level === 3);
          
          setDownline(l1Users);
          setLevel2Downline(l2Users);
          setLevel3Downline(l3Users);

          // Fetch sponsor name
          if (profile.sponsorId && profile.sponsorId !== 'admin') {
            const sponsorDoc = await sanityClient.fetch(`*[_type == "user" && (referralCode == $sid || _id == $sid)][0]`, { sid: profile.sponsorId });
            if (sponsorDoc) {
              setSponsorName(sponsorDoc.displayName || 'Unknown');
            }
          }
        }
      } catch (err: any) {
        console.error("Missing Sanity Project ID or API Token. Please check your environment variables.", err);
        // Fallback for dashboard error state
        alert("Missing Sanity Project ID or API Token. Please check your environment variables.");
      } finally {
        setLoading(false);
      }
    };'''
content = content.replace(old_fetchData, new_fetchData)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
