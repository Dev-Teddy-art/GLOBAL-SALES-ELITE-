import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# I will find the exact block and replace it manually.
start_str = "        {/* Network Section */}"
end_str = "        <CommissionCalculator"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_network = '''        {/* Network Section */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">
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
        </div>
'''
    content = content[:start_idx] + new_network + content[end_idx:]

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
