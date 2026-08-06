import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Replace NetworkTreeView
old_network = '''function NetworkTreeView({ users }: { users: (UserProfile & { id: string })[] }) {
  // Build tree
  const tree: Record<string, (UserProfile & { id: string })[]> = {};
  users.forEach(u => {
    const parentId = u.sponsorId || 'admin';
    if (!tree[parentId]) tree[parentId] = [];
    tree[parentId].push(u);
  });

  const calculateNetworkSize = (userId: string): number => {
    const children = tree[userId] || [];
    let size = children.length;
    for (const child of children) {
      size += calculateNetworkSize(child.id);
    }
    return size;
  };

  const getSponsorName = (sponsorId: string) => {
    if (!sponsorId || sponsorId === 'admin') return 'None (Admin)';
    const sponsor = users.find(u => u.referralCode === sponsorId || u.id === sponsorId);
    return sponsor ? sponsor.displayName : sponsorId;
  };

  const flattenedUsers: (UserProfile & { id: string, depth: number })[] = [];
  const traverse = (nodeId: string, depth: number) => {
    const children = tree[nodeId] || [];
    for (const child of children) {
      flattenedUsers.push({ ...child, depth });
      traverse(child.id, depth + 1);
    }
  };
  traverse('admin', 0);
  
  // Add any orphans that might not have been caught
  users.forEach(u => {
    if (!flattenedUsers.find(fu => fu.id === u.id)) {
      flattenedUsers.push({ ...u, depth: 0 });
    }
  });

  return (
    <div className="overflow-x-auto bg-white rounded-xl border border-gray-100 shadow-sm">
      <table className="min-w-full text-left text-sm whitespace-nowrap">
        <thead className="bg-gray-50 uppercase tracking-wider text-gray-500 font-semibold border-b border-gray-100">
          <tr>
            <th className="px-6 py-4">User Name</th>
            <th className="px-6 py-4">Email</th>
            <th className="px-6 py-4">Sponsor (Parent)</th>
            <th className="px-6 py-4">Ref Code</th>
            <th className="px-6 py-4 text-center">Network Size</th>
            <th className="px-6 py-4">Joined Date</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100 text-gray-700">
          {flattenedUsers.map((user, index) => (
            <motion.tr 
              key={user.id} 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="hover:bg-gray-50 transition-colors"
            >
              <td className="px-6 py-4 font-medium flex items-center gap-3" style={{ paddingLeft: `calc(1.5rem + ${user.depth * 2.5}rem)` }}>
                {user.depth > 0 && (
                  <div className="text-gray-300 flex-shrink-0 -ml-6 mr-1">
                    <CornerDownRight size={18} />
                  </div>
                )}
                <div className={`h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold ${user.isAdmin || user.role === 'admin' ? 'bg-amber-100 text-amber-700' : 'bg-[#070b5e]/10 text-[#070b5e]'}`}>
                  {user.isAdmin || user.role === 'admin' ? <Shield size={14} /> : user.displayName.charAt(0).toUpperCase()}
                </div>
                {user.displayName} {user.isAdmin || user.role === 'admin' ? <span className="ml-1 text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full">Admin</span> : ''}
              </td>
              <td className="px-6 py-4">{user.email}</td>
              <td className="px-6 py-4 text-gray-500">{getSponsorName(user.sponsorId)}</td>
              <td className="px-6 py-4"><span className="text-xs font-medium text-[#e03126] bg-red-50 px-2 py-0.5 rounded border border-red-100">{user.referralCode}</span></td>
              <td className="px-6 py-4 text-center">
                <span className="inline-flex items-center justify-center bg-gray-100 px-3 py-1 rounded-full font-bold text-gray-700">
                  {calculateNetworkSize(user.id)}
                </span>
              </td>
              <td className="px-6 py-4 text-gray-500">
                {user.createdAt ? new Date(user.createdAt).toLocaleDateString() : 'N/A'}
              </td>
            </motion.tr>
          ))}
          {users.length === 0 && (
            <tr>
              <td colSpan={6} className="px-6 py-8 text-center text-gray-400">
                No users found in the system.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}'''

new_network = '''import { ReferralTree } from './ReferralTree';

function NetworkTreeView({ users }: { users: (UserProfile & { id: string })[] }) {
  return <ReferralTree users={users} isAdminView={true} />;
}'''

content = content.replace(old_network, new_network)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
