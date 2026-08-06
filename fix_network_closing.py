import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

old_net = '''        {/* Network Section */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.3 }} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">
          <div className="flex items-center gap-3 mb-6 border-b border-gray-100 pb-4">
            <Network className="text-[#070b5e]" size={28} />
            <h3 className="text-xl font-bold text-gray-900">
              {profile.role === 'admin' ? 'Global Network Tree' : 'Your Downline'}
            </h3>
          </div>
          
          <ReferralTree 
            users={allUsers} 
            rootUserId={profile.role === 'admin' ? undefined : (profile.id || profile._id)} 
            isAdminView={profile.role === 'admin' || profile.isAdmin}
          />
        </div>'''

new_net = '''        {/* Network Section */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.3 }} className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6 md:p-8 relative overflow-hidden">
          <div className="flex items-center gap-4 mb-6 border-b border-gray-100 pb-6 relative z-10">
            <div className="bg-[#070b5e]/10 p-3 rounded-2xl text-[#070b5e]">
              <Network size={28} />
            </div>
            <div>
              <h3 className="text-2xl font-black text-gray-900 tracking-tight">
                {profile.role === 'admin' ? 'Global Network Tree' : 'Your Downline'}
              </h3>
              <p className="text-gray-500 text-sm font-medium mt-1">Explore and manage your connections</p>
            </div>
          </div>
          
          <div className="relative z-10">
            <ReferralTree 
              users={allUsers} 
              rootUserId={profile.role === 'admin' ? undefined : (profile.id || profile._id)} 
              isAdminView={profile.role === 'admin' || profile.isAdmin}
            />
          </div>
        </motion.div>'''

if old_net in content:
    content = content.replace(old_net, new_net)
else:
    print("Could not find old network block")

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
