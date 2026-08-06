import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Add a modal for User Management
state_additions = """
  const [editingUser, setEditingUser] = useState<any>(null);
  const [editForm, setEditForm] = useState<any>({});
"""

content = content.replace("const [loading, setLoading] = useState(true);", "const [loading, setLoading] = useState(true);\n" + state_additions)

# Add edit user logic
logic = """
  const handleSaveUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingUser) return;
    try {
      const res = await fetch('/api/admin/update-user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ adminId: profile?._id, userId: editingUser.id, updates: editForm })
      });
      if (res.ok) {
        setUsers(users.map(u => u.id === editingUser.id ? { ...u, ...editForm } : u));
        setEditingUser(null);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggleBan = async (user: any) => {
    const isBanned = user.status === 'banned';
    try {
      const res = await fetch('/api/admin/ban-user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ adminId: profile?._id, userId: user.id, banned: !isBanned })
      });
      if (res.ok) {
        setUsers(users.map(u => u.id === user.id ? { ...u, status: !isBanned ? 'banned' : 'active' } : u));
        if (editingUser?.id === user.id) {
          setEditingUser({ ...editingUser, status: !isBanned ? 'banned' : 'active' });
        }
      }
    } catch (err) {
      console.error(err);
    }
  };
"""

content = content.replace("  if (!profile || (profile.role !== 'admin' && !profile.isAdmin)) return null;", logic + "\n  if (!profile || (profile.role !== 'admin' && !profile.isAdmin)) return null;")

# Update the focused area
old_focused = """          <span className="text-sm text-[#EF4444]">Focused: <strong>{nodeMap.get(focusedId)?.displayName}</strong></span>
          <button 
            onClick={() => setFocusedId(null)}
            className="text-xs bg-[#EF4444] text-gray-900 dark:text-white px-2 py-1 rounded hover:bg-[#EF4444] transition-colors"
          >
            Reset
          </button>"""
          
new_focused = """          <span className="text-sm text-[#EF4444]">Focused: <strong>{nodeMap.get(focusedId)?.displayName}</strong></span>
          <button 
            onClick={() => {
              const u = nodeMap.get(focusedId);
              if (u) {
                setEditingUser(u);
                setEditForm({ firstName: u.firstName || '', lastName: u.lastName || '', email: u.email || '', bankName: u.bankName || '', bankAccountNumber: u.bankAccountNumber || '' });
              }
            }}
            className="text-xs bg-blue-600 text-white px-3 py-1 rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
          >
            Manage User
          </button>
          <button 
            onClick={() => setFocusedId(null)}
            className="text-xs bg-gray-200 dark:bg-gray-800 text-gray-900 dark:text-white px-3 py-1 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors"
          >
            Reset
          </button>"""

content = content.replace(old_focused, new_focused)

# Add Modal JSX at the end of the return
modal_jsx = """      {/* User Management Modal */}
      <AnimatePresence>
        {editingUser && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
            <motion.div 
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="absolute inset-0 bg-black/60 backdrop-blur-sm"
              onClick={() => setEditingUser(null)}
            />
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 rounded-2xl shadow-2xl p-6 w-full max-w-lg relative z-10"
            >
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">Manage User</h2>
                <button onClick={() => setEditingUser(null)} className="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                  ✕
                </button>
              </div>
              
              <form onSubmit={handleSaveUser} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-gray-500 dark:text-gray-400 mb-1">First Name</label>
                    <input type="text" value={editForm.firstName} onChange={e => setEditForm({...editForm, firstName: e.target.value})} className="w-full bg-gray-50 dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-xl px-3 py-2 text-sm text-gray-900 dark:text-white outline-none focus:border-[#EF4444]" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 dark:text-gray-400 mb-1">Last Name</label>
                    <input type="text" value={editForm.lastName} onChange={e => setEditForm({...editForm, lastName: e.target.value})} className="w-full bg-gray-50 dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-xl px-3 py-2 text-sm text-gray-900 dark:text-white outline-none focus:border-[#EF4444]" />
                  </div>
                </div>
                
                <div>
                  <label className="block text-xs font-bold text-gray-500 dark:text-gray-400 mb-1">Email</label>
                  <input type="email" value={editForm.email} onChange={e => setEditForm({...editForm, email: e.target.value})} className="w-full bg-gray-50 dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-xl px-3 py-2 text-sm text-gray-900 dark:text-white outline-none focus:border-[#EF4444]" />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-gray-500 dark:text-gray-400 mb-1">Bank Name</label>
                    <input type="text" value={editForm.bankName} onChange={e => setEditForm({...editForm, bankName: e.target.value})} className="w-full bg-gray-50 dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-xl px-3 py-2 text-sm text-gray-900 dark:text-white outline-none focus:border-[#EF4444]" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 dark:text-gray-400 mb-1">Account Number</label>
                    <input type="text" value={editForm.bankAccountNumber} onChange={e => setEditForm({...editForm, bankAccountNumber: e.target.value})} className="w-full bg-gray-50 dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-xl px-3 py-2 text-sm text-gray-900 dark:text-white outline-none focus:border-[#EF4444]" />
                  </div>
                </div>
                
                <div className="pt-4 border-t border-gray-200 dark:border-white/10 flex justify-between items-center">
                  <button
                    type="button"
                    onClick={() => handleToggleBan(editingUser)}
                    className={`px-4 py-2 rounded-xl text-sm font-bold shadow-sm transition-colors ${editingUser.status === 'banned' ? 'bg-green-100 text-green-700 hover:bg-green-200' : 'bg-red-100 text-red-700 hover:bg-red-200'}`}
                  >
                    {editingUser.status === 'banned' ? 'Unban User' : 'Ban User'}
                  </button>
                  <button type="submit" className="bg-[#EF4444] text-white px-6 py-2 rounded-xl text-sm font-bold hover:bg-red-600 transition-colors shadow-lg">
                    Save Changes
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
"""

content = content.replace("    </div>\n  );\n}\n", "    </div>\n" + modal_jsx + "  );\n}\n")

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)

