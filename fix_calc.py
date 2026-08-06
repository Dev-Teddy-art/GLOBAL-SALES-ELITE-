import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

start_str = '    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">'
end_str = '  );\n}\n\nexport function Dashboard()'

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_calc = '''    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }} className="bg-white rounded-3xl shadow-lg border border-gray-100 p-8 md:p-10 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-blue-50 to-transparent opacity-50 pointer-events-none" />
      <div className="flex items-center gap-4 mb-8 relative z-10">
        <div className="bg-gradient-to-br from-[#070b5e] to-[#0a0f82] p-3.5 rounded-2xl shadow-md text-white">
          <Calculator size={28} />
        </div>
        <div>
          <h3 className="text-2xl font-black text-gray-900 tracking-tight">
            Potential Earnings
          </h3>
          <p className="text-gray-500 text-sm font-medium">Model your network commissions</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 relative z-10">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">Average Sale Value (₦)</label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 font-bold">₦</span>
              <input 
                type="number" 
                min="0"
                value={avgSaleValue || ''}
                onChange={(e) => setAvgSaleValue(Math.max(0, parseInt(e.target.value) || 0))}
                placeholder="1000"
                className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl pl-10 pr-4 py-3.5 focus:ring-2 focus:ring-[#070b5e] focus:border-transparent outline-none transition-all font-mono font-bold"
              />
            </div>
          </div>
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-bold text-gray-700">Level 1 Members</label>
              <span className="text-[10px] uppercase tracking-widest font-black text-green-700 bg-green-100 px-2.5 py-1 rounded-full">5% Comm.</span>
            </div>
            <input 
              type="number" 
              min="0"
              value={l1Count || ''}
              onChange={(e) => setL1Count(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="0"
              className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3.5 focus:ring-2 focus:ring-[#070b5e] focus:border-transparent outline-none transition-all font-mono font-bold"
            />
          </div>
          
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-bold text-gray-700">Level 2 Members</label>
              <span className="text-[10px] uppercase tracking-widest font-black text-blue-700 bg-blue-100 px-2.5 py-1 rounded-full">2% Comm.</span>
            </div>
            <input 
              type="number" 
              min="0"
              value={l2Count || ''}
              onChange={(e) => setL2Count(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="0"
              className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3.5 focus:ring-2 focus:ring-[#070b5e] focus:border-transparent outline-none transition-all font-mono font-bold"
            />
          </div>
          {role === 'admin' && (
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-bold text-gray-700">Level 3 Members</label>
                <span className="text-[10px] uppercase tracking-widest font-black text-amber-700 bg-amber-100 px-2.5 py-1 rounded-full">1% Comm.</span>
              </div>
              <input 
                type="number" 
                min="0"
                value={l3Count || ''}
                onChange={(e) => setL3Count(Math.max(0, parseInt(e.target.value) || 0))}
                placeholder="0"
                className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3.5 focus:ring-2 focus:ring-[#070b5e] focus:border-transparent outline-none transition-all font-mono font-bold"
              />
            </div>
          )}
        </div>
        <div className="bg-gradient-to-br from-[#070b5e] to-[#0a0f82] text-white rounded-3xl p-8 flex flex-col justify-center items-center text-center shadow-2xl relative overflow-hidden group border border-[#070b5e]/20">
          <div className="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-[#e03126] opacity-30 rounded-full blur-2xl group-hover:scale-125 group-hover:opacity-40 transition-all duration-700 pointer-events-none" />
          
          <span className="text-white/80 font-bold uppercase tracking-widest text-xs mb-4 z-10">Estimated Monthly Earnings</span>
          <span className="text-4xl md:text-5xl lg:text-6xl font-black text-white drop-shadow-md mb-6 z-10 font-mono tracking-tighter">
            {currencyFormatter.format(totalEarnings).replace('NGN', '₦').trim()}
          </span>
          <div className="h-1.5 w-12 bg-gradient-to-r from-[#e03126] to-red-400 rounded-full mb-6 z-10" />
          <p className="text-white/70 text-sm max-w-[250px] font-medium z-10 leading-relaxed">
            This is an estimate based on {role === 'admin' ? '3' : '2'} levels of your network downline.
          </p>
        </div>
      </div>
    </motion.div>
'''
    
    content = content[:start_idx] + new_calc + content[end_idx:]
    with open('src/components/Dashboard.tsx', 'w') as f:
        f.write(content)
else:
    print("Could not find start or end index for calculator", start_idx, end_idx)
