import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

old_header = '''        {/* Header Section */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8 flex flex-col md:flex-row gap-6 justify-between items-start md:items-center">
          <div>
            <h2 className="text-2xl font-black text-gray-900 mb-1">
              {isFirstLogin ? 'Welcome' : 'Welcome back'}, {profile.firstName || profile.displayName?.split(' ')[0]}
            </h2>
            <p className="text-gray-500">
              {profile.isAdmin || profile.role === 'admin' 
                ? "You have full visibility over the network tree." 
                : `Your sponsor is: ${sponsorName}`}
            </p>
          </div>
          <div className="bg-red-50 border border-red-100 rounded-xl p-4 flex flex-col gap-2 min-w-[300px]">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-[#e03126] uppercase tracking-wider flex items-center gap-2">
                <LinkIcon size={16} /> Your Referral Link
              </span>
            </div>
            <div className="flex items-center gap-2 mt-1">
              <input 
                type="text" 
                readOnly 
                value={`${window.location.origin}/signup?ref=${profile?.referralCode}`}
                className="flex-1 bg-white border border-gray-200 text-sm text-gray-600 rounded px-3 py-2 outline-none"
              />
              <button 
                onClick={copyReferralLink}
                className="bg-[#070b5e] hover:bg-[#050845] text-white p-2 rounded transition-colors"
              >
                <Copy size={18} />
              </button>
            </div>
          </div>
        </div>'''

new_header = '''        {/* Header Section */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }} className="bg-gradient-to-br from-[#070b5e] to-[#0a0f82] rounded-3xl shadow-xl border border-[#070b5e]/20 p-8 md:p-10 flex flex-col md:flex-row gap-8 justify-between items-start md:items-center relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-16 -mr-16 w-64 h-64 bg-white opacity-5 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 left-0 -mb-16 -ml-16 w-48 h-48 bg-[#e03126] opacity-10 rounded-full blur-2xl pointer-events-none" />
          
          <div className="relative z-10 text-white">
            <h2 className="text-3xl md:text-4xl font-black mb-2 tracking-tight drop-shadow-sm">
              {isFirstLogin ? 'Welcome' : 'Welcome back'}, <span className="text-[#e03126]">{profile.firstName || profile.displayName?.split(' ')[0]}</span>
            </h2>
            <p className="text-white/80 text-lg max-w-xl font-medium">
              {profile.isAdmin || profile.role === 'admin' 
                ? "You have full administrative access to monitor and manage the Global Sales Elite network." 
                : `Continue building your network. Your current sponsor is ${sponsorName}.`}
            </p>
          </div>
          
          <div className="relative z-10 bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-5 flex flex-col gap-3 min-w-[320px] shadow-2xl">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white/90 uppercase tracking-widest flex items-center gap-2">
                <LinkIcon size={14} className="text-[#e03126]" /> Your Referral Link
              </span>
            </div>
            <div className="flex items-center gap-2">
              <input 
                type="text" 
                readOnly 
                value={`${window.location.origin}/signup?ref=${profile?.referralCode}`}
                className="flex-1 bg-white/10 border border-white/20 text-sm text-white rounded-xl px-4 py-3 outline-none focus:border-white/40 transition-colors font-mono"
              />
              <button 
                onClick={copyReferralLink}
                className="bg-[#e03126] hover:bg-[#c9291f] text-white p-3 rounded-xl transition-colors shadow-lg hover:shadow-xl hover:-translate-y-0.5 duration-200"
              >
                <Copy size={18} />
              </button>
            </div>
          </div>
        </motion.div>'''

if old_header in content:
    content = content.replace(old_header, new_header)
else:
    print("Could not find old header block")

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
