import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

old_sales = """  return (
    <>
      <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col h-[380px] relative z-10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <DollarSign className="text-[#0F172A] dark:text-white" size={20} />
            Sales & Commission Requests
          </h3>
          <span className="bg-[#EF4444] text-gray-900 dark:text-white text-xs font-bold px-2.5 py-1 rounded-full">{sales.length}</span>
        </div>
        
        <div className="flex-1 overflow-auto custom-scrollbar pr-2 space-y-3">
          {loading ? (
            <div className="text-gray-500 text-center py-10 text-sm">Loading...</div>
          ) : sales.length === 0 ? (
            <div className="text-gray-500 dark:text-gray-500 text-center py-10 text-sm">No pending payouts.</div>
          ) : (
            sales.map((w) => (
              <motion.div 
                key={w._id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/5 rounded-xl p-3 flex justify-between items-center group hover:border-[#EF4444]/30 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-[#EF4444]/10 flex items-center justify-center text-[#EF4444]">
                    <DollarSign size={16} />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-gray-900 dark:text-white leading-none">{w.userRef?.displayName}</p>
                    <p className="text-xs text-gray-500 mt-1">Sold: ₦{w.amount.toLocaleString()} • {w.userRef?.bankName}</p>
                    <p className="text-xs text-gray-400 font-mono mt-0.5">{w.userRef?.bankAccountNumber}</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => handleProcess(w._id, 'approved')} className="text-xs font-bold bg-green-500/10 text-green-600 hover:bg-green-500 hover:text-white px-3 py-1.5 rounded-lg transition-colors">
                    Approve
                  </button>
                  <button onClick={() => handleProcess(w._id, 'rejected')} className="text-xs font-bold bg-red-500/10 text-red-600 hover:bg-red-500 hover:text-white px-3 py-1.5 rounded-lg transition-colors">
                    Reject
                  </button>
                </div>
              </motion.div>
            ))
          )}
        </div>
      </div>
    </>
  );"""

new_sales = """  return (
    <>
      <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col h-[380px] relative z-10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <DollarSign className="text-[#0F172A] dark:text-white" size={20} />
            Sales & Commission Requests
          </h3>
          <span className="bg-[#EF4444] text-white text-xs font-bold px-2.5 py-1 rounded-full">{sales.length}</span>
        </div>
        
        <div className="flex-1 overflow-auto custom-scrollbar pr-2 space-y-3">
          {loading ? (
            <div className="text-gray-500 text-center py-10 text-sm">Loading...</div>
          ) : sales.length === 0 ? (
            <div className="text-gray-500 dark:text-gray-500 text-center py-10 text-sm">No sales logged yet.</div>
          ) : (
            sales.map((w) => (
              <motion.div 
                key={w._id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/5 rounded-xl p-4 flex flex-col gap-3 group hover:border-[#EF4444]/30 transition-colors"
              >
                <div className="flex justify-between items-start">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-[#10B981]/10 flex items-center justify-center text-[#10B981]">
                      <DollarSign size={20} />
                    </div>
                    <div>
                      <p className="text-sm font-bold text-gray-900 dark:text-white leading-none">{w.propertyName || 'Property Sale'}</p>
                      <p className="text-xs text-gray-500 mt-1">Sold by: <strong>{w.userRef?.displayName}</strong></p>
                      <p className="text-xs text-gray-500 mt-0.5">Date: {w.dateSold ? new Date(w.dateSold).toLocaleDateString() : 'N/A'}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-black text-gray-900 dark:text-white">₦{w.amount?.toLocaleString()}</p>
                    {w.status === 'pending' ? (
                      <span className="inline-block mt-1 px-2 py-0.5 bg-yellow-100 text-yellow-800 text-[10px] font-bold rounded">PENDING</span>
                    ) : w.status === 'approved' ? (
                      <span className="inline-block mt-1 px-2 py-0.5 bg-green-100 text-green-800 text-[10px] font-bold rounded">APPROVED</span>
                    ) : (
                      <span className="inline-block mt-1 px-2 py-0.5 bg-red-100 text-red-800 text-[10px] font-bold rounded">REJECTED</span>
                    )}
                  </div>
                </div>
                
                <div className="bg-gray-100 dark:bg-[#0F172A] p-2 rounded-lg flex justify-between items-center text-xs">
                  <div>
                    <span className="text-gray-500">Bank:</span> <span className="font-bold text-gray-700 dark:text-gray-300">{w.userRef?.bankName || 'N/A'}</span>
                    <span className="mx-2 text-gray-300">|</span>
                    <span className="text-gray-500">Acc:</span> <span className="font-mono text-gray-700 dark:text-gray-300">{w.userRef?.bankAccountNumber || 'N/A'}</span>
                  </div>
                </div>

                {w.status === 'pending' && (
                  <div className="flex gap-2 justify-end mt-1">
                    <button onClick={() => handleProcess(w._id, 'approved')} className="text-xs font-bold bg-[#10B981] text-white hover:bg-[#059669] px-4 py-1.5 rounded-lg transition-colors shadow-sm">
                      Mark Paid
                    </button>
                    <button onClick={() => handleProcess(w._id, 'rejected')} className="text-xs font-bold bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 px-4 py-1.5 rounded-lg transition-colors">
                      Reject
                    </button>
                  </div>
                )}
              </motion.div>
            ))
          )}
        </div>
      </div>
    </>
  );"""

content = content.replace(old_sales, new_sales)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
