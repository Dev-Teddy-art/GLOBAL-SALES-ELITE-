import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

old_calc = '''    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">
      <div className="flex items-center gap-3 mb-6 border-b border-gray-100 pb-4">
        <Calculator className="text-[#070b5e]" size={28} />
        <h3 className="text-xl font-bold text-gray-900">
          Potential Earnings Calculator
        </h3>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Average Sale Value (₦)</label>
            <input 
              type="number" 
              min="0"
              value={avgSaleValue || ''}
              onChange={(e) => setAvgSaleValue(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="1000"
              className="w-full bg-white border border-gray-300 text-gray-900 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#070b5e] outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Level 1 Members (Direct Referrals) - 5% commission</label>
            <input 
              type="number" 
              min="0"
              value={l1Count || ''}
              onChange={(e) => setL1Count(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="0"
              className="w-full bg-white border border-gray-300 text-gray-900 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#070b5e] outline-none"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Level 2 Members - 2% commission</label>
            <input 
              type="number" 
              min="0"
              value={l2Count || ''}
              onChange={(e) => setL2Count(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="0"
              className="w-full bg-white border border-gray-300 text-gray-900 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#070b5e] outline-none"
            />
          </div>
          {role === 'admin' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Level 3 Members - 1% commission</label>
              <input 
                type="number" 
                min="0"
                value={l3Count || ''}
                onChange={(e) => setL3Count(Math.max(0, parseInt(e.target.value) || 0))}
                placeholder="0"
                className="w-full bg-white border border-gray-300 text-gray-900 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#070b5e] outline-none"
              />
            </div>
          )}
        </div>
        <div className="bg-[#070b5e] text-white rounded-xl p-6 flex flex-col justify-center items-center text-center shadow-inner">
          <span className="text-white/80 font-medium uppercase tracking-wider text-sm mb-2">Estimated Potential Earnings</span>
          <span className="text-4xl md:text-5xl font-black text-[#e03126] drop-shadow-sm mb-4">
            {currencyFormatter.format(totalEarnings)}
          </span>
          <p className="text-white/70 text-sm max-w-xs">
            This is an estimate based on {role === 'admin' ? '3' : '2'} levels of your network downline.
          </p>
        </div>
      </div>
    </motion.div>'''

new_calc = '''    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }} className="bg-white rounded-3xl shadow-lg border border-gray-100 p-8 md:p-10">
      <div className="flex items-center gap-4 mb-8">
        <div className="bg-[#070b5e]/10 p-3 rounded-2xl">
          <Calculator className="text-[#070b5e]" size={28} />
        </div>
        <div>
          <h3 className="text-2xl font-black text-gray-900">
            Potential Earnings
          </h3>
          <p className="text-gray-500 text-sm font-medium">Calculate your network commission</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">Average Sale Value (₦)</label>
            <input 
              type="number" 
              min="0"
              value={avgSaleValue || ''}
              onChange={(e) => setAvgSaleValue(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="1000"
              className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#070b5e] focus:border-transparent outline-none transition-all font-mono"
            />
          </div>
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-bold text-gray-700">Level 1 Members</label>
              <span className="text-xs font-bold text-green-600 bg-green-50 px-2 py-1 rounded-md">5% Comm.</span>
            </div>
            <input 
              type="number" 
              min="0"
              value={l1Count || ''}
              onChange={(e) => setL1Count(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="0"
              className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#070b5e] focus:border-transparent outline-none transition-all font-mono"
            />
          </div>
          
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-bold text-gray-700">Level 2 Members</label>
              <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded-md">2% Comm.</span>
            </div>
            <input 
              type="number" 
              min="0"
              value={l2Count || ''}
              onChange={(e) => setL2Count(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="0"
              className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#070b5e] focus:border-transparent outline-none transition-all font-mono"
            />
          </div>
          {role === 'admin' && (
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-bold text-gray-700">Level 3 Members</label>
                <span className="text-xs font-bold text-amber-600 bg-amber-50 px-2 py-1 rounded-md">1% Comm.</span>
              </div>
              <input 
                type="number" 
                min="0"
                value={l3Count || ''}
                onChange={(e) => setL3Count(Math.max(0, parseInt(e.target.value) || 0))}
                placeholder="0"
                className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#070b5e] focus:border-transparent outline-none transition-all font-mono"
              />
            </div>
          )}
        </div>
        <div className="bg-gradient-to-br from-[#070b5e] to-[#0a0f82] text-white rounded-3xl p-8 flex flex-col justify-center items-center text-center shadow-xl relative overflow-hidden group">
          <div className="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-[#e03126] opacity-20 rounded-full blur-2xl group-hover:scale-110 transition-transform duration-500" />
          
          <span className="text-white/80 font-bold uppercase tracking-widest text-xs mb-3 z-10">Estimated Monthly Earnings</span>
          <span className="text-4xl md:text-5xl lg:text-6xl font-black text-white drop-shadow-md mb-6 z-10 font-mono tracking-tight">
            {currencyFormatter.format(totalEarnings).replace('NGN', '₦').trim()}
          </span>
          <div className="h-1 w-16 bg-[#e03126] rounded-full mb-6 z-10" />
          <p className="text-white/70 text-sm max-w-xs font-medium z-10">
            This is an estimate based on {role === 'admin' ? '3' : '2'} levels of your network downline.
          </p>
        </div>
      </div>
    </motion.div>'''

if old_calc in content:
    content = content.replace(old_calc, new_calc)
else:
    print("Could not find old calculator block")

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
