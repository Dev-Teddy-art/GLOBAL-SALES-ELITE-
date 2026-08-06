import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

new_table = """
function SalesHistoryTable({ sales }: { sales: any[] }) {
  return (
    <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col w-full mt-8 relative z-10">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
          <Database className="text-[#0F172A] dark:text-white" size={20} />
          Full Sales History & Payouts
        </h3>
      </div>
      
      <div className="overflow-x-auto w-full">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-gray-200 dark:border-white/10">
              <th className="py-3 px-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Realtor Name</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Property</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Amount (₦)</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Date</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-500 uppercase tracking-widest text-right">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-white/5">
            {sales.length === 0 ? (
              <tr>
                <td colSpan={5} className="py-8 text-center text-sm text-gray-500">No sales recorded yet.</td>
              </tr>
            ) : (
              sales.map((s) => (
                <tr key={s._id} className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                  <td className="py-3 px-4 text-sm font-bold text-gray-900 dark:text-white">
                    {s.userRef?.displayName || 'Unknown'}
                  </td>
                  <td className="py-3 px-4 text-sm text-gray-700 dark:text-gray-300">
                    {s.propertyName || 'N/A'}
                  </td>
                  <td className="py-3 px-4 text-sm font-mono text-gray-900 dark:text-white">
                    ₦{s.amount?.toLocaleString()}
                  </td>
                  <td className="py-3 px-4 text-sm text-gray-500">
                    {s.dateSold ? new Date(s.dateSold).toLocaleDateString() : 'N/A'}
                  </td>
                  <td className="py-3 px-4 text-right">
                    {s.status === 'pending' ? (
                      <span className="inline-block px-2 py-1 bg-yellow-100 text-yellow-800 text-[10px] font-bold rounded">PENDING</span>
                    ) : s.status === 'approved' ? (
                      <span className="inline-block px-2 py-1 bg-green-100 text-green-800 text-[10px] font-bold rounded">APPROVED</span>
                    ) : (
                      <span className="inline-block px-2 py-1 bg-red-100 text-red-800 text-[10px] font-bold rounded">REJECTED</span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""

if 'function SalesHistoryTable' not in content:
    content = content.replace("function SalesApprovals", new_table + "\nfunction SalesApprovals")

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
